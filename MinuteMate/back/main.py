### IMPORTS ###
import os
from dotenv import load_dotenv
from typing import Optional, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
# import ssl 
import logging
logging.basicConfig(level=logging.INFO)
import weaviate
from weaviate.classes.init import Auth
# from weaviate.classes.query import Rerank, MetadataQuery
import openai
from openai import OpenAI
from rake_nltk import Rake
import nltk  # TODO are we actually using NLTK?
try:
    nltk.download('punkt')
    nltk.download('punkt_tab')
    nltk.download('stopwords')
except Exception as e:
    print(f"Error downloading NLTK resources: {e}")

### CONSTANTS ###
SEARCH_TYPES = {
        'keyword': 'bm25',
        'vector': 'near_vector',
        'hybrid': 'hybrid'
    }
DEFAULT_WEAVIATE_COLLECTION_NAME = 'MeetingDocument'
DEFAULT_OPENAI_EMBEDDING_MODEL = 'text-embedding-3-small'
DEFAULT_OPENAI_GENERATIVE_MODEL = 'gpt-4o'


### COMMON RESOURCES AND INITIALIZATION ###
# LOGGING
# https://docs.python.org/3/library/logging.html
logger = logging.getLogger(__name__)

# API
app = FastAPI(
    title="MinuteMate Prompt & Response API",
    description="An AI-powered API for processing meeting-related prompts",
    version="1.0.0"
).add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# ENVIRONMENTAL VARIABLES
load_dotenv()

WEAVIATE_ENDPOINT_URL = os.environ.get('WEAVIATE_ENDPOINT_URL')
WEAVIATE_API_KEY = os.environ.get('WEAVIATE_API_KEY')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# VECTOR DATABASE
weaviate_client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_ENDPOINT_URL,
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    additional_config=weaviate.classes.init.AdditionalConfig(
        timeout=weaviate.classes.init.Timeout(init=10, query=30)))

# EMBEDDING SERVICE

embedding_client = OpenAI(
    api_key = OPENAI_API_KEY
)

# GENERATIVE SERVICE
generative_client = OpenAI(
    api_key = OPENAI_API_KEY
)

# NATURAL LANGUAGE PROCESSING TOOLS
rake = Rake()


### REQUEST AND RESPONSE MODELS
class PromptRequest(BaseModel):
    user_prompt_text: str = Field(..., min_length=1, max_length=1000)

# TODO does this need to be based on BaseModel?
# TODO Can we just return a list of 3-tuples instead?
class ContextSegment(BaseModel):
    chunk_id: int
    content: str
    score: Optional[float] = None

class PromptResponse(BaseModel):
    generated_response: str
    context_segments: List[ContextSegment] = []
    keywords: List[str] = []
    error_code: int = 0


# Establish secure socket layer?
# TODO - figure out how this works,
# TODO - ensure that this does work 
# TODO - ensure it's in the right place
# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
 
# TODO clarify how this works
# TODO clarify whether an object initialization is necessary & eliminate if possible
def extract_keywords(text: str) -> List[str]:
        """Extract keywords using RAKE"""
        try:
            # Extract keywords, return ranked phrases    
            rake.extract_keywords_from_text(text)
            return rake.get_ranked_phrases()[:3]
        
        except Exception as e:
            logger.error(f"Keyword extraction error: {e}")
            return []

def search_weaviate(
        query: str, 
        search_type: str,
        target_collection_name : str = DEFAULT_WEAVIATE_COLLECTION_NAME) -> List[ContextSegment]:
    
    """
    Search Weaviate database
    """
    
    # Search Weaviate
    try:
        collection = weaviate_client.collections.get(target_collection_name)
        
        if search_type == 'keyword':
            keywords = extract_keywords(query)
            results = collection.query.bm25(
                query=",".join(keywords),
                limit=5
            )
            # print(keywords)
        
        elif search_type == 'vector':
            
            embedding = embedding_client.embeddings.create(
                model=DEFAULT_OPENAI_EMBEDDING_MODEL,
                input=query
            ).data[0].embedding
            
            results = collection.query.near_vector(
                near_vector=embedding,
                limit=5
            )

        else:
            raise ValueError(f"Unsupported search type: {search_type}")

        context_segments =  [
            ContextSegment(
                chunk_id=int(item.properties.get('chunk_id', 0)),
                content=item.properties.get('content', ''),
                score=getattr(item.metadata, 'distance', None)
            ) for item in results.objects
        ]
        
        #TODO do we need to return keywords here?
        return context_segments, keywords
    
    except Exception as e:
        logger.error(f"Weaviate search error: {e}")
        return []

def openai_generate_with_context(
        prompt: str, 
        context: List[ContextSegment] = [],
        model = DEFAULT_OPENAI_GENERATIVE_MODEL) -> str:
    
    """Generate response using OpenAI"""
    
    # Merge RAG context
    # TODO see if generative models supports specific tokens 
    # for identifying context segments & if so implement them
    context_text = "\n".join([
        f"<ContextSegment{seg.chunk_id}>\n{seg.content}" 
        for seg in context
    ])

    try:
        # Call the generative service to get a chat response
        # Provide initial chat prompt as well as added context
        response = generative_client.chat.completions.create(
            model = model,
            messages=[
                {
                    "role": "system", 
                    "content": f"Use this context if relevant: {context_text}"
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


def main_response(prompt_request: PromptRequest) -> PromptResponse:
    """Main method to process prompts"""

    ### 1- INITIAL TRUST AND SAFETY CHECK ###
    # TODO add initial trust & safety check here
    # If trust and safety check fails, return the error immediately

    generated_response = None

    ### 2- INFORMATION RETRIEVAL ###
    try:
        # Search for relevant context
        context_segments, keywords = search_weaviate(prompt_request.user_prompt_text)
    except Exception as e:
        logger.error(f"Response information retrieval error: {e}")
        return PromptResponse(
            generated_response="An error occurred while processing your request.",
            error_code=500)

    ### 3 - RESPONSE GENERATION ### 
    # Generate response to user with OpenAI generative model
    # https://platform.openai.com/docs/api-reference/chat/create
    
    try:
        generated_response = openai_generate_with_context(
            prompt_request.user_prompt_text, 
            context_segments,
            model = DEFAULT_OPENAI_GENERATIVE_MODEL)
        
    except Exception as e:
        logger.error(f"Response content generation error: {e}")
        return PromptResponse(
            generated_response="An error occurred while processing your request.",
            error_code=500)


    ### 4 - FINAL TRUST AND SAFETY CHECK ###
    # TODO add final trust & safety check here
    # If trust and safety check fails, return an error


    ### 5 - BUILD & RETURN RESPONSE OBJECT ###
    # Return chat response to API layer
    # to be passed along to frontend
    #TODO there aren't necessarily going to be keywords
    return PromptResponse(
            generated_response=generated_response,
            context_segments=context_segments,
            keywords = keywords,
            error_code=0
        )

# API Endpoint
@app.post("/process-prompt", response_model=PromptResponse)
async def process_prompt_endpoint(prompt_request: PromptRequest):
    """Process user prompt and return response"""
    return main_response(prompt_request)


# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    """Close Weaviate connection on app shutdown"""
    weaviate_client.close()