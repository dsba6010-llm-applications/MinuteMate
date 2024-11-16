from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

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
    response = ''

    #Call whatever code we need to here

    return response

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
