import os
from openai import OpenAI
import weaviate
import tiktoken  # Use tiktoken for OpenAI-compatible tokenization
from utils.env_setup import load_env
from utils.azure_blob_utils import download_from_azure

# Load environment variables
load_env()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Weaviate client
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
)

# Initialize OpenAI client for embedding
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize tiktoken for OpenAI's embedding model
tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")


def fetch_matching_chunks(meeting_date, meeting_type, file_type, source_document):
    """
    Fetch matching chunks from Weaviate based on metadata.

    Args:
        meeting_date (str): Date of the meeting.
        meeting_type (str): Type of the meeting (e.g., "Board of Commissioners").
        file_type (str): File type (e.g., "Minutes").
        source_document (str): Name of the source document.

    Returns:
        list: A list of matching documents.
    """
    query = f"""
    {{
        Get {{
            MeetingDocument(where: {{
                operator: And,
                operands: [
                    {{ path: ["meeting_date"], operator: Equal, valueString: "{meeting_date}" }},
                    {{ path: ["meeting_type"], operator: Equal, valueString: "{meeting_type}" }},
                    {{ path: ["file_type"], operator: Equal, valueString: "{file_type}" }},
                    {{ path: ["source_document"], operator: Equal, valueString: "{source_document}" }}
                ]
            }}) {{
                _additional {{
                    id
                }}
            }}
        }}
    }}
    """
    response = client.query.raw(query)
    return response.get("data", {}).get("Get", {}).get("MeetingDocument", [])


def delete_matching_chunks(documents):
    """
    Delete matching chunks from Weaviate.

    Args:
        documents (list): List of documents with IDs to delete.
    """
    for doc in documents:
        doc_id = doc["_additional"]["id"]
        client.data_object.delete(doc_id)
        print(f"Deleted chunk ID: {doc_id}")


def tokenize_and_embed_text(clean_file_name, metadata, max_chunk_size=250):
    """
    Tokenizes, chunks, and embeds cleaned text into Weaviate.

    Args:
        clean_file_name (str): Name of the cleaned text file in Azure Blob Storage (clean folder).
        metadata (dict): Metadata associated with the file (meeting_date, meeting_type, file_type).
        max_chunk_size (int): Maximum token size for each chunk.
    """
    try:
        # Download cleaned text from Azure
        clean_text = download_from_azure("clean", clean_file_name)
        tokens = tokenizer.encode(clean_text)
        chunks = [
            tokenizer.decode(tokens[i:i + max_chunk_size])
            for i in range(0, len(tokens), max_chunk_size)
        ]

        # Metadata fields
        meeting_date = str(metadata["meeting_date"])
        meeting_type = metadata["meeting_type"]
        file_type = metadata["file_type"]
        source_document = clean_file_name

        # Check for existing embeddings
        matching_chunks = fetch_matching_chunks(meeting_date, meeting_type, file_type, source_document)
        if matching_chunks:
            print(f"Found {len(matching_chunks)} existing chunks. Deleting...")
            delete_matching_chunks(matching_chunks)
        else:
            print("No existing chunks found.")

        # Embed and upload each chunk
        for i, chunk in enumerate(chunks):
            response = openai_client.embeddings.create(input=chunk, model="text-embedding-ada-002")
            embedding = response.data[0].embedding

            client.data_object.create(
                data_object={
                    "content": chunk,
                    "meeting_date": meeting_date,
                    "meeting_type": meeting_type,
                    "file_type": file_type,
                    "chunk_index": i,
                    "source_document": source_document
                },
                vector=embedding,
                class_name="MeetingDocument"
            )
            print(f"Uploaded chunk {i + 1}/{len(chunks)} to Weaviate.")

        print("Successfully processed and embedded all chunks.")

    except Exception as e:
        print(f"Error during tokenization and embedding: {e}")
