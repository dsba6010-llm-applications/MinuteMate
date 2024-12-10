import streamlit as st
import tiktoken  # For OpenAI-compatible tokenization
from openai import OpenAI
from utils.azure_blob_utils import download_from_azure

# Initialize tiktoken for OpenAI's GPT models
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")  # Specify the OpenAI model


def get_openai_client():
    """
    Retrieves the OpenAI client using the API key from Streamlit session state.

    Returns:
        OpenAI: OpenAI client object.
    """
    api_keys = st.session_state.get("api_keys", {})
    openai_api_key = api_keys.get("OPENAI_API_KEY")

    if not openai_api_key:
        raise ValueError("OpenAI API Key is missing. Please configure it on the Home Page.")

    return OpenAI(api_key=openai_api_key)


def tokenize_and_split_text(text, max_chunk_size=250):
    """
    Tokenizes and splits text into smaller chunks within the token size limit.

    Args:
        text (str): The text to split.
        max_chunk_size (int): Maximum token size for each chunk.

    Returns:
        list of str: List of smaller text chunks.
    """
    # Validate text input
    if not text or text.strip() == "":
        raise ValueError("Text input is empty or invalid.")

    # Tokenize the text into tokens
    tokens = tokenizer.encode(text)

    # Split tokens into chunks of max_chunk_size
    chunks = [
        tokenizer.decode(tokens[i:i + max_chunk_size])
        for i in range(0, len(tokens), max_chunk_size)
    ]
    return chunks


def clean_text_chunk(chunk, openai_client):
    """
    Cleans a single chunk of text using OpenAI GPT.

    Args:
        chunk (str): Text chunk to clean.
        openai_client (OpenAI): OpenAI client instance.

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

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=2000,
            temperature=0.5
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error during chunk cleaning: {e}")
        return f"Error in chunk cleaning: {e}"


def clean_text(dirty_file_name):
    """
    Cleans the given text file by splitting it into smaller chunks and processing each chunk.

    Args:
        dirty_file_name (str): Name of the file in Azure Blob Storage (dirty folder).

    Returns:
        str: Combined cleaned text.
    """
    try:
        print(f"Downloading {dirty_file_name} from Azure Blob Storage (dirty folder)...")
        dirty_content = download_from_azure("dirty", dirty_file_name)

        # Validate dirty content
        if not dirty_content or dirty_content.strip() == "":
            raise ValueError("The downloaded content is empty. Please check the file content.")

        # Initialize OpenAI client dynamically
        openai_client = get_openai_client()

        # Tokenize and split the text into chunks
        print("Tokenizing and splitting text into manageable chunks...")
        chunks = tokenize_and_split_text(dirty_content, max_chunk_size=250)
        cleaned_chunks = []

        for i, chunk in enumerate(chunks):
            print(f"Cleaning chunk {i + 1}/{len(chunks)}: {chunk[:100]}...")
            try:
                cleaned_chunk = clean_text_chunk(chunk, openai_client)
            except Exception as e:
                print(f"Error cleaning chunk {i + 1}: {e}")
                cleaned_chunk = f"Error cleaning this chunk: {e}"

            if not cleaned_chunk.strip():
                print(f"Chunk {i + 1} returned empty after cleaning.")
                raise ValueError(f"Chunk {i + 1} cleaning failed. Received empty content.")
            
            cleaned_chunks.append(cleaned_chunk)

        print(f"Successfully cleaned {len(chunks)} chunks.")
        return "\n\n".join(cleaned_chunks)

    except Exception as e:
        print(f"Error during text cleaning: {e}")
        return None

