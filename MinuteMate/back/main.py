import os
import logging
from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import Rerank, MetadataQuery

import openai
from openai import OpenAI

from rake_nltk import Rake
from dotenv import load_dotenv

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
except Exception as e:
    print(f"Error downloading NLTK resources: {e}")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize the FastAPI app
app = FastAPI(
    title="MinuteMate Prompt & Response API",
    description="An AI-powered API for processing meeting-related prompts",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Update ContextSegment to include a metadata dictionary
class ContextSegment(BaseModel):
    chunk_id: int
    content: str
    score: Optional[float] = None
    metadata: Optional[dict] = None  # Add metadata support

class PromptRequest(BaseModel):
    user_prompt_text: str = Field(..., min_length=1, max_length=1000)

class PromptResponse(BaseModel):
    generated_response: str
    context_segments: List[ContextSegment] = []
    keywords: List[str] = []
    error_code: int = 0

class WeaviateConfig:
    """Configuration for Weaviate connection and querying"""
    SEARCH_TYPES = {
        'keyword': 'bm25',
        'vector': 'near_vector',
        'hybrid': 'hybrid'
    }

    @classmethod
    def get_weaviate_client(cls, url: str, api_key: str):
        """Establish Weaviate connection"""
        try:
            return weaviate.connect_to_weaviate_cloud(
                cluster_url=url,
                auth_credentials=Auth.api_key(api_key),
                additional_config=weaviate.classes.init.AdditionalConfig(
                    timeout=weaviate.classes.init.Timeout(init=10, query=30)
                )
            )
        except Exception as e:
            logger.error(f"Weaviate connection error: {e}")
            raise

class PromptProcessor:
    """Main class for processing user prompts"""
    def __init__(self):
        # Load environment variables
        self.load_env_vars()
        
        # Initialize clients
        self.weaviate_client = WeaviateConfig.get_weaviate_client(
            self.WEAVIATE_ENDPOINT_URL, 
            self.WEAVIATE_API_KEY
        )
        self.openai_client = OpenAI(api_key=self.OPENAI_API_KEY)

    def load_env_vars(self):
        """Load and validate environment variables"""
        required_vars = [
            'OPENAI_API_KEY', 
            'WEAVIATE_ENDPOINT_URL', 
            'WEAVIATE_API_KEY'
        ]
        
        for var in required_vars:
            value = os.getenv(var)
            print(f"Loading {var}: {value}")
            if not value:
                raise ValueError(f"Missing environment variable: {var}")
            setattr(self, var, value)

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords using RAKE"""
        try:
            rake = Rake()
            rake.extract_keywords_from_text(text)
            return rake.get_ranked_phrases()[:3]
        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []

    def search_weaviate(self, query: str, search_type: str = 'keyword'):
        """Perform search in Weaviate database"""
        try:
            collection = self.weaviate_client.collections.get('MeetingDocument')
            
            if search_type == 'keyword':
                keywords = self.extract_keywords(query)
                results = collection.query.bm25(
                    query=",".join(keywords),
                    limit=5
                )
            elif search_type == 'vector':
                embedding = self.openai_client.embeddings.create(
                    model='text-embedding-3-small',
                    input=query
                ).data[0].embedding
                
                results = collection.query.near_vector(
                    near_vector=embedding,
                    limit=5
                )
            else:
                raise ValueError(f"Unsupported search type: {search_type}")

            # Extract metadata fields from properties
            # Make sure these fields exist in your Weaviate schema and data.
            context_segments = [
                ContextSegment(
                    chunk_id=int(item.properties.get('chunk_id', 0)),
                    content=item.properties.get('content', ''),
                    score=getattr(item.metadata, 'distance', None),
                    metadata={
                        "meeting_date": item.properties.get('meeting_date', ''),
                        "meeting_type": item.properties.get('meeting_type', ''),
                        "file_type": item.properties.get('file_type', ''),
                        "chunk_index": item.properties.get('chunk_index', ''),
                        "source_document": item.properties.get('source_document', '')
                    }
                ) for item in results.objects
            ]

            keywords = self.extract_keywords(query)  # Ensure keywords are returned even for vector search
            return context_segments, keywords
        except Exception as e:
            logger.error(f"Weaviate search error: {e}")
            return [], []

    def generate_response(self, prompt: str, context_segments: List[ContextSegment]) -> str:
        """Generate response using OpenAI"""

        # Include metadata in the context to help the LLM make more informed decisions
        context_text_list = []
        for seg in context_segments:
            meta = seg.metadata if seg.metadata else {}
            context_text_list.append(
                f"<ContextSegment{seg.chunk_id}>\n"
                f"Content: {seg.content}\n"
                f"Meeting Date: {meta.get('meeting_date', 'N/A')}\n"
                f"Meeting Type: {meta.get('meeting_type', 'N/A')}\n"
                f"File Type: {meta.get('file_type', 'N/A')}\n"
                f"Chunk Index: {meta.get('chunk_index', 'N/A')}\n"
                f"Source Document: {meta.get('source_document', 'N/A')}\n"
            )

        context_text = "\n".join(context_text_list)

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": (
                            "You are an assistant that uses retrieved meeting data with metadata. "
                            "Consider the given context segments and their metadata to provide a more accurate and informed response. "
                            "If the metadata (like meeting_date, meeting_type, etc.) is relevant, incorporate it into your answer.\n\n"
                            f"Use this context if relevant:\n{context_text}"
                        )
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            )
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return "I'm sorry, but I couldn't generate a response."

    def check_prompt(self, prompt: str) -> str:
        """Check prompt appropriateness using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": """A local government hosts a chat system that uses retrieval-augmented generation 
                        to improve public access to the contents of its public meetings... (same instructions)"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            )
            if response.choices[0].message.content.split(maxsplit=1)[0] in {'appropriate', 'inappropriate', 'ambiguous'}:
                return response.choices[0].message.content
            else:
                return 'error generating prompt check'
        
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return "I'm sorry, but I couldn't generate a response."

    def check_response(self, prompt: str) -> str:
        """Check response appropriateness using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system", 
                        "content": """A local government hosts a chat system... (same instructions)"""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            )
            if response.choices[0].message.content.split(maxsplit=1)[0] in {'appropriate', 'inappropriate', 'ambiguous'}:
                return response.choices[0].message.content
            else:
                return 'error generating response check'
        
        except Exception as e:
            logger.error(f"OpenAI generation error: {e}")
            return "I'm sorry, but I couldn't generate a response."

    def process_prompt(self, prompt_request: PromptRequest) -> PromptResponse:
        """Main method to process user prompt"""
        try:
            # Check the user prompt for inappropriate content
            prompt_check = self.check_prompt(prompt_request.user_prompt_text)
            if prompt_check.split(maxsplit=1)[0] == 'inappropriate':
                return PromptResponse(generated_response='inappropriate prompt detected')

            # Search for relevant context
            context_segments, keywords = self.search_weaviate(prompt_request.user_prompt_text)
            
            # Generate response
            generated_response = self.generate_response(
                prompt_request.user_prompt_text, 
                context_segments
            )

            # Check the generated response for inappropriate content
            response_check = self.check_response(prompt_request.user_prompt_text)
            if response_check.split(maxsplit=1)[0] == 'inappropriate':
                return PromptResponse(generated_response='inappropriate response detected')

            return PromptResponse(
                generated_response=generated_response,
                context_segments=context_segments,
                keywords=keywords,
                error_code=0
            )

        except Exception as e:
            logger.error(f"Prompt processing error: {e}")
            return PromptResponse(
                generated_response="An error occurred while processing your request.",
                error_code=500
            )

# Initialize processor
processor = PromptProcessor()

# API Endpoint
@app.post("/process-prompt", response_model=PromptResponse)
async def process_prompt_endpoint(prompt_request: PromptRequest):
    """Process user prompt and return response"""
    return processor.process_prompt(prompt_request)

# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Close Weaviate connection on app shutdown"""
    processor.weaviate_client.close()
