from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv
import chardet
load_dotenv()  # Load environment variables from .env file

# Set up the blob service client
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
container_name = os.getenv("AZURE_STORAGE_CONTAINER")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_client = blob_service_client.get_container_client(container_name)

def upload_to_azure(folder_name, file_name, file_content):
    """
    Upload a file to Azure Blob Storage.

    Args:
        folder_name (str): The folder in the Azure container (e.g., raw, dirty, clean).
        file_name (str): The name of the file to upload.
        file_content (bytes): The binary content of the file to upload.
    """
    blob_name = f"{folder_name}/{file_name}"
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(file_content, overwrite=True)
    print(f"Uploaded to Azure: {blob_name}")

def download_from_azure(folder_name, file_name, as_text=True):
    """
    Download a file from Azure Blob Storage with streaming.
    """
    blob_name = f"{folder_name}/{file_name}"
    blob_client = container_client.get_blob_client(blob_name)

    # Print the URL for debugging
    print(f"Generated Blob URL: {blob_client.url}")

    try:
        downloader = blob_client.download_blob(max_concurrency=5)
        if as_text:
            # Read as binary first and detect encoding
            raw_data = downloader.readall()
            detected_encoding = chardet.detect(raw_data)['encoding']
            print(f"Detected encoding: {detected_encoding}")
            return raw_data.decode(detected_encoding)  # Decode using detected encoding
        else:
            print(f"Downloading {blob_name} as binary.")
            return downloader.readall()  # Return binary content
    except Exception as e:
        print(f"Error downloading blob {blob_name}: {e}")
        raise e


def list_blobs_in_folder(folder_name):
    """
    List all blobs in a specific folder in Azure Blob Storage.

    Args:
        folder_name (str): The folder to list blobs from.

    Returns:
        list: List of blob names.
    """
    blobs = container_client.list_blobs(name_starts_with=f"{folder_name}/")
    return [blob.name for blob in blobs]
