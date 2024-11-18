import weaviate
import os
from utils.env_setup import load_env
from utils.azure_blob_utils import download_from_azure

# Load environment variables
load_env()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Set up the Weaviate client with API key authentication
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
)

def process_and_embed_text(clean_file_name, metadata, chunk_size=500):
    """
    Combines chunking and embedding into a single process:
    - Splits the cleaned text into smaller chunks.
    - Embeds each chunk into Weaviate with metadata.

    Parameters:
    - clean_file_name: str, name of the cleaned text file in Azure Blob Storage (clean folder).
    - metadata: dict, metadata associated with each chunk (e.g., meeting date, type, etc.).
    - chunk_size: int, number of words per chunk.
    """
    try:
        # Step 1: Download the cleaned text from Azure and chunk it
        print(f"Downloading and chunking the text from {clean_file_name}...")
        clean_text = download_from_azure("clean", clean_file_name)
        words = clean_text.split()
        chunks = [" ".join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

        # Extract metadata
        meeting_date = str(metadata["meeting_date"])
        meeting_type = metadata["meeting_type"]
        file_type = metadata["file_type"]

        # Step 2: Check for existing documents in Weaviate with the same metadata and delete them
        query = f"""
        {{
            Get {{
                MeetingDocument(where: {{
                    path: ["meeting_date", "meeting_type", "file_type"],
                    operator: And,
                    valueString: "{meeting_date}"
                }}) {{
                    id
                }}
            }}
        }}
        """
        response = client.query.raw(query)
        existing_documents = response.get("data", {}).get("Get", {}).get("MeetingDocument", [])

        # Step 3: Delete any existing documents with matching metadata in Weaviate
        for doc in existing_documents:
            client.data_object.delete(doc["id"])
        print(f"Deleted {len(existing_documents)} existing documents with matching metadata.")

        # Step 4: Embed and store new chunks in Weaviate
        for chunk in chunks:
            client.data_object.create(
                data_object={
                    "content": chunk,
                    "meeting_date": meeting_date,
                    "meeting_type": meeting_type,
                    "file_type": file_type
                },
                class_name="MeetingDocument"
            )
            print(f"Embedded chunk for {clean_file_name} in Weaviate.")

        print(f"Successfully embedded {len(chunks)} chunks for {clean_file_name}.")

    except Exception as e:
        print(f"Error during chunking and embedding: {e}")
