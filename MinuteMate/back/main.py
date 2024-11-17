from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from weaviate.classes.query import Rerank, MetadataQuery
import os
import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.init import AdditionalConfig, Timeout
from rake_nltk import Rake
import nltk
nltk.download('stopwords')
nltk.download('punkt')


weaviate_url = os.environ["WEAVIATE_URL"]
weaviate_api_key = os.environ["WEAVIATE_API_KEY"]
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=weaviate_url,
    auth_credentials=Auth.api_key(weaviate_api_key),
)

# Initialize the FastAPI app
app = FastAPI(
    title="MinuteMate Propmpt & Response API",
    description="A simple API that takes a text prompt uses ",
    version="1.0.0" 

)

# Define the request schema
class PromptRequest(BaseModel):
    prompt: str

# Define the response schema
class PromptResponse(BaseModel):
    response: str

# Your Python processing logic
def process_prompt(prompt: str) -> str:
    rake = Rake()
    rake.extract_keywords_from_text(prompt)
    return rake.get_ranked_phrases()[:3] 
    

# API endpoint
@app.post("/process-prompt", response_model=PromptResponse)
async def process_prompt_endpoint(request: PromptRequest):
    """
    Process the prompt and return the response
    """
    try:
        result = process_prompt(request.prompt)
        return PromptResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# This is the code to get the collections based on top 3 keywords we are fetching from the RAKE code. 
# You can add this code block below wherever you are configuring your API
collection = client.collections.get("MeetingDocument")
response = collection.query.bm25(
    query=",".join(keywords),
    limit=5,
    # rerank=Rerank(
    #     prop="content",
    #     query="meeting"
    # ),
    # return_metadata=MetadataQuery(score=True)
)

for o in response.objects:
    print(o.properties)
    # print(o.metadata.rerank_score)
