# This allows you to test out deleted specific meeting date, meeting types, file type chunks. 

import os
import weaviate
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEAVIATE_URL = os.getenv("WEAVIATE_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

# Initialize Weaviate client
client = weaviate.Client(
    url=WEAVIATE_URL,
    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY)
)

def fetch_documents(date, meeting_type, file_type):
    """
    Fetch documents from Weaviate based on specific criteria.

    Args:
        date (str): The date to filter by (YYYY-MM-DD format).
        meeting_type (str): The meeting type to filter by (e.g., "Board of Commissioners").
        file_type (str): The file type to filter by (e.g., "Minutes").

    Returns:
        list: A list of matching documents.
    """
    query = f"""
    {{
        Get {{
            MeetingDocument(where: {{
                operator: And,
                operands: [
                    {{
                        path: ["meeting_date"],
                        operator: Equal,
                        valueString: "{date}"
                    }},
                    {{
                        path: ["meeting_type"],
                        operator: Equal,
                        valueString: "{meeting_type}"
                    }},
                    {{
                        path: ["file_type"],
                        operator: Equal,
                        valueString: "{file_type}"
                    }}
                ]
            }}) {{
                _additional {{
                    id
                }}
                meeting_date
                meeting_type
                file_type
                chunk_index
                content
            }}
        }}
    }}
    """
    response = client.query.raw(query)
    documents = response.get("data", {}).get("Get", {}).get("MeetingDocument", [])
    return documents

def delete_documents(documents):
    """
    Delete all documents in the provided list from Weaviate.

    Args:
        documents (list): A list of documents with `_additional.id` to delete.
    """
    for doc in documents:
        doc_id = doc.get("_additional", {}).get("id")
        if doc_id:
            client.data_object.delete(doc_id)
            print(f"Deleted document ID: {doc_id}")
        else:
            print("Document ID not found; skipping deletion.")

if __name__ == "__main__":
    # Specify the criteria for deletion
    specific_date = "2000-10-27"
    specific_meeting_type = "Board of Commissioners"
    specific_file_type = "Minutes"

    # Step 1: Fetch documents
    print(f"Fetching documents for {specific_date}, {specific_meeting_type}, {specific_file_type}...")
    matching_documents = fetch_documents(specific_date, specific_meeting_type, specific_file_type)
    if matching_documents:
        print(f"\nFound {len(matching_documents)} matching documents:")
        for doc in matching_documents:
            print(f"- ID: {doc.get('_additional', {}).get('id')}")
            print(f"  Chunk Index: {doc.get('chunk_index', 'N/A')}")
            print(f"  Meeting Date: {doc.get('meeting_date', 'N/A')}")
            print(f"  Meeting Type: {doc.get('meeting_type', 'N/A')}")
            print(f"  File Type: {doc.get('file_type', 'N/A')}")
            print(f"  Content Preview: {doc.get('content', 'N/A')[:100]}...")
            print()
    else:
        print("No matching documents found.")

    # Step 2: Delete documents
    if matching_documents:
        print("Deleting matching documents...")
        delete_documents(matching_documents)

    # Step 3: Confirm deletion by re-fetching
    print(f"Fetching documents again for {specific_date}, {specific_meeting_type}, {specific_file_type}...")
    remaining_documents = fetch_documents(specific_date, specific_meeting_type, specific_file_type)
    if remaining_documents:
        print(f"\nFound {len(remaining_documents)} remaining documents (deletion failed for some):")
        for doc in remaining_documents:
            print(f"- ID: {doc.get('_additional', {}).get('id')}")
            print(f"  Chunk Index: {doc.get('chunk_index', 'N/A')}")
            print(f"  Meeting Date: {doc.get('meeting_date', 'N/A')}")
            print(f"  Meeting Type: {doc.get('meeting_type', 'N/A')}")
            print(f"  File Type: {doc.get('file_type', 'N/A')}")
            print(f"  Content Preview: {doc.get('content', 'N/A')[:100]}...")
            print()
    else:
        print("All matching documents have been successfully deleted.")
