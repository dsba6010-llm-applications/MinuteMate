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

def tokenize_and_embed_text(clean_file_name, metadata, max_chunk_size=250):
    """
    Tokenizes, chunks, and embeds cleaned text into Weaviate.

    Args:
        clean_file_name (str): Name of the cleaned text file in Azure Blob Storage (clean folder).
        metadata (dict): Metadata associated with the file (meeting_date, meeting_type, file_type).
        max_chunk_size (int): Maximum token size for each chunk.
    """
    try:
        # Step 1: Download cleaned text from Azure
        clean_text = download_from_azure("clean", clean_file_name)
        print(f"Downloaded cleaned text from Azure for file: {clean_file_name}")

        # Step 2: Tokenize the text using tiktoken
        tokens = tokenizer.encode(clean_text)

        # Step 3: Chunk tokens into groups of max_chunk_size (default: 250 tokens per chunk)
        chunks = [
            tokenizer.decode(tokens[i:i + max_chunk_size])
            for i in range(0, len(tokens), max_chunk_size)
        ]
        print(f"Tokenized and split text into {len(chunks)} chunks of {max_chunk_size} tokens each.")

        # Extract metadata for embedding
        meeting_date = str(metadata["meeting_date"])
        meeting_type = metadata["meeting_type"]
        file_type = metadata["file_type"]

        # Step 4: Check and delete existing embeddings in Weaviate (to prevent duplication)
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

        for doc in existing_documents:
            client.data_object.delete(doc["id"])
        print(f"Deleted {len(existing_documents)} existing embeddings for this file.")

        # Step 5: Embed each chunk using OpenAI and store in Weaviate
        for i, chunk in enumerate(chunks):
            # Generate embedding using OpenAI
            response = openai_client.embeddings.create(
                input=chunk,
                model="text-embedding-ada-002"
            )
            embedding = response.data[0].embedding  # Correctly access embedding from the response object

            # Upload chunk to Weaviate
            client.data_object.create(
                data_object={
                    "content": chunk,
                    "meeting_date": meeting_date,
                    "meeting_type": meeting_type,
                    "file_type": file_type,
                    "chunk_index": i  # Include chunk index for ordering
                },
                vector=embedding,
                class_name="MeetingDocument"
            )
            print(f"Uploaded chunk {i+1}/{len(chunks)} to Weaviate.")

        print("Successfully processed and embedded all chunks.")

    except Exception as e:
        print(f"Error during tokenization and embedding: {e}")
