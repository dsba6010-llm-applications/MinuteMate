import weaviate
import os
from utils.env_setup import load_env

# Load environment variables
load_env()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Set up the Weaviate client with API key authentication
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
)

def embed_text(chunks, metadata):
    """
    Embeds text chunks and stores them in Weaviate with metadata.

    Parameters:
    - chunks: list of str, text chunks to embed
    - metadata: dict, metadata associated with each chunk
    """
    for chunk in chunks:
        client.data_object.create(
            data_object={
                "content": chunk,
                "meeting_date": str(metadata["meeting_date"]),
                "meeting_type": metadata["meeting_type"],
                "file_type": metadata["file_type"]
            },
            class_name="MeetingDocument"
        )
