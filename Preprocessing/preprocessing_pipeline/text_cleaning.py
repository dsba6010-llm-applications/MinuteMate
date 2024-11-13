import os
from openai import OpenAI
from utils.env_setup import load_env

# Load environment variables
load_env()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def clean_text(dirty_text):
    # Context to guide the model
    context_prompt = (
        "The following text is a transcription of a municipal meeting for the town of Cramerton. "
        "The transcription quality may be poor, and some words, like the town's name, Cramerton, "
        "may not have been transcribed correctly. If you encounter words that seem out of place or incorrect, "
        "please correct them based on this context."
    )
    
    # Full prompt including context and original transcription
    messages = [
        {"role": "system", "content": context_prompt},
        {"role": "user", "content": f"Clean the following text for readability and correct errors: {dirty_text}"}
    ]
    
    # Create a chat completion with the specified model
    response = client.chat.completions.create(
        model="gpt-4",  # Specify the model, e.g., gpt-4 or gpt-3.5-turbo
        messages=messages,
        max_tokens=500,
        temperature=0.5
    )
    
    # Extract and return the response text
    return response.choices[0].message.content.strip()
