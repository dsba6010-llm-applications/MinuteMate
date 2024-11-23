from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import os

from rake_nltk import Rake

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.init import AdditionalConfig
from weaviate.classes.init import Timeout
from weaviate.classes.query import Rerank
from weaviate.classes.query import MetadataQuery

import openai
from openai import OpenAI


# Initialize the FastAPI app
app = FastAPI(
    title="MinuteMate Propmpt & Response API",
    description="A simple API that takes a text prompt uses ",
    version="1.0.0" 

)

# Define the request schema
class PromptRequest(BaseModel):
    user_prompt_text: str

# Define the response schema
class PromptResponse(BaseModel):
    generated_response: str
    error_code : int

# Takes a prompt from the front end, processes the prompt
# using NLP tools, embedding services, and generative services
# and finally returns the prompt response
def process_prompt(prompt_request: PromptRequest) -> PromptResponse:

    ### 0 - ENVIRONMENT AND CONFIGURATION ###

    # Update environment variables
    # not sure if this works
    # TODO test and/or look for alternatives
    import os  

    # Set API keys, endpoint URLs, model versions, and configurations
    # Embedding and Generative Models
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    # OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL')
    OPENAI_EMBEDDING_URL = os.getenv('OPENAI_EMBEDDING_URL')
    OPENAI_GENERATION_URL = os.getenv('OPENAI_GENERATION_URL')
    EMBEDDING_MODEL = 'text-embedding-3-small'
    ENCODING_FORMAT = 'float'
    RESPONDING_GENERATIVE_MODEL = 'gpt-4o'
    # TRUSTSAFETY_GENERATIVE_MODEL = llama on modal, probably, but can't be too
                                      
    # API key, endpoint URL, and target collection(s)
    # for Weaviate vector database
    WEAVIATE_URL = os.environ['WEAVIATE_URL']
    WEAVIATE_API_KEY = os.environ['WEAVIATE_API_KEY']
    WEAVIATE_TARGET_COLLECTION = 'MeetingDocument'
    # WEAVIATE_TARGET_COLLECTION = "VERBA_Embedding_text_embedding_3_small"



    ### 1- INITIAL TRUST AND SAFETY CHECK ###
    # TODO add initial trust & safety check here
    # If trust and safety check fails, return the error immediately



    ### 2- INFORMATION RETRIEVAL ###

    # Set RAG search type
    SEARCH_TYPE = 'keyword'
    # SEARCH_TYPE = 'vector'
    # SEARCH_TYPE = 'hybrid'
    
    # Establish connection with Weaviate server
    # https://weaviate.io/developers/weaviate
    weaviate_client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),
    ) 
    # Look up the appropriate Weviate database collection
    db_collection = weaviate_client.collections.get(WEAVIATE_TARGET_COLLECTION)
    db_response = None

    # Extract keywords and query database
    #  TODO - finish and test
    if(SEARCH_TYPE == 'keyword'):
        
        rake = Rake()
        rake.extract_keywords_from_text(prompt_request.user_prompt_text)
        keywords = rake.get_ranked_phrases()[:3]
        db_response = db_collection.query.bm25(
            query=",".join(keywords),
            limit=5,
            # rerank=Rerank(
            #     prop="content",
            #     query="meeting"
            # ),
        # return_metadata=MetadataQuery(score=True)
        )

    # Vectorize the prompt and query the database
    # TODO - test
    elif(SEARCH_TYPE == 'vector'):
        

        # Set API Key.  Not necessary if you have an 
        # OPENAI_API_KEY variable in your environment
        openai.api_key = OPENAI_API_KEY 
        embedding_client = OpenAI()

        # Vector-embed the prompt
        embedding_response = embedding_client.embeddings.create(
            model = EMBEDDING_MODEL,
            input = prompt_request.user_prompt_text,
            encoding_format = ENCODING_FORMAT
        )

        # Extract the vector embeddings list[float] from the embedding response
        query_vector = embedding_response.data[0].embedding 
        
        # Send vector query to database and get response
        db_response = db_collection.query.near_vector(
            near_vector=query_vector,
            limit=10,
            return_metadata=MetadataQuery(distance=True)
        )

    #TODO support this   
    #elif(SEARCH_TYPE == 'hybrid'):
    

    else:
        #No RAG search
        db_response = None

    # Extract items from database response 
    # and aggregate into a single string 
    db_response_text = ""
    for item in db_response.objects:
        segment = '\n<ContextSegment' + str(int(item.properties.get('chunk_id'))) + '>\n'
        db_response_text += segment
        db_response_text += item.properties.get('content')


    ### 3 - RESPONSE GENERATION ### 

    # Generate response to user with OpenAI generative model
    # https://platform.openai.com/docs/api-reference/chat/create
    openai.api_key = OPENAI_API_KEY 
    generation_client = OpenAI()
    generated_response_text = generation_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
            "role": "system", 
            "content": f"You are a helpful assistant who uses this context if appropriate: {db_response_text}"
            },
            {
            "role": "user", 
            "content": prompt_request.user_prompt_text 
            }
        ]
    )

    ### 4 - FINAL TRUST AND SAFETY CHECK ###
    # TODO add final trust & safety check here
    # If trust and safety check fails, return an error
    

    ### 5 - BUILD & RETURN RESPONSE OBJECT ###
    # Return chat response to API layer
    # to be passed along to frontend
    prompt_response = PromptResponse()
    prompt_response.generated_response = generated_response_text
    return prompt_response


    
    

# API endpoint
@app.post("/process-prompt", response_model=PromptResponse)
async def process_prompt_endpoint(prompt_request: PromptRequest):
    """
    Process the prompt and return the response
    """
    try:
        prompt_response = process_prompt(prompt_request)
        return PromptResponse(result=prompt_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    