import os
from openai import OpenAI
from utils.env_setup import load_env
from utils.azure_blob_utils import download_from_azure, upload_to_azure

# Load environment variables
load_env()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def split_text(text, max_chunk_size=3000):
    """
    Splits a large text into smaller chunks, each within the specified token size.

    Args:
        text (str): The text to split.
        max_chunk_size (int): Maximum token size for each chunk.

    Returns:
        list of str: List of smaller text chunks.
    """
    chunks = []
    words = text.split()
    chunk = []
    current_size = 0

    for word in words:
        current_size += len(word) + 1  # +1 accounts for spaces
        if current_size > max_chunk_size:
            chunks.append(" ".join(chunk))
            chunk = []
            current_size = len(word) + 1
        chunk.append(word)

    if chunk:
        chunks.append(" ".join(chunk))

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
        model="gpt-4",
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
    
    # Split the text into chunks
    chunks = split_text(dirty_content, max_chunk_size=3000)
    cleaned_chunks = []

    for i, chunk in enumerate(chunks):
        print(f"Cleaning chunk {i + 1}/{len(chunks)}...")
        cleaned_chunk = clean_text_chunk(chunk)
        cleaned_chunks.append(cleaned_chunk)

    return "\n\n".join(cleaned_chunks)
