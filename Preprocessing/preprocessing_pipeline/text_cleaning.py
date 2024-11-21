import os
from openai import OpenAI
import tiktoken  # Use tiktoken for OpenAI-compatible tokenization
from utils.env_setup import load_env
from utils.azure_blob_utils import download_from_azure, upload_to_azure

# Load environment variables
load_env()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize tiktoken for OpenAI's GPT models
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Specify the OpenAI model

def tokenize_and_split_text(text, max_chunk_size=250):
    """
    Tokenizes and splits text into smaller chunks within the token size limit.

    Args:
        text (str): The text to split.
        max_chunk_size (int): Maximum token size for each chunk.

    Returns:
        list of str: List of smaller text chunks.
    """
    # Tokenize the text into tokens
    tokens = tokenizer.encode(text)

    # Split tokens into chunks of max_chunk_size
    chunks = [
        tokenizer.decode(tokens[i:i + max_chunk_size])
        for i in range(0, len(tokens), max_chunk_size)
    ]
    return chunks

def clean_text_chunk(chunk):
    """
    Cleans a single chunk of text using OpenAI GPT.

    Args:
        chunk (str): Text chunk to clean.

    Returns:
        str: Cleaned text.
    """
    context_prompt = (
        "The following text is a transcription of a municipal meeting for the town of Cramerton. "
        "Please clean it for readability and correct any errors or inconsistencies."
    )
    messages = [
        {"role": "system", "content": context_prompt},
        {"role": "user", "content": f"Clean the following text for readability: {chunk}"}
    ]

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def clean_text(dirty_file_name):
    """
    Cleans the given text file by splitting it into smaller chunks and processing each chunk.

    Args:
        dirty_file_name (str): Name of the file in Azure Blob Storage (dirty folder).

    Returns:
        str: Combined cleaned text.
    """
    print(f"Downloading {dirty_file_name} from Azure Blob Storage...")
    dirty_content = download_from_azure("dirty", dirty_file_name)
    
    # Tokenize and split the text into chunks of 250 tokens
    chunks = tokenize_and_split_text(dirty_content, max_chunk_size=250)
    cleaned_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"Cleaning chunk {i + 1}/{len(chunks)}...")
        cleaned_chunk = clean_text_chunk(chunk)
        cleaned_chunks.append(cleaned_chunk)

    return "\n\n".join(cleaned_chunks)
