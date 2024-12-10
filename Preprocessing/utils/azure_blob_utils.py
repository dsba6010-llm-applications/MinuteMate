from azure.storage.blob import BlobServiceClient
import chardet
import streamlit as st

def get_blob_service_clients():
    """
    Initializes the Azure Blob Service Client and Container Client dynamically from `st.session_state`.

    Returns:
        tuple: (BlobServiceClient, ContainerClient)
    """
    try:
        api_keys = st.session_state.get("api_keys", {})
        connection_string = api_keys.get("AZURE_STORAGE_CONNECTION_STRING")
        container_name = api_keys.get("AZURE_STORAGE_CONTAINER")

        if not connection_string:
            raise ValueError("Azure Storage Connection String is missing. Please set it on the Home Page.")
        if not container_name:
            raise ValueError("Azure Storage Container Name is missing. Please set it on the Home Page.")

        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(container_name)
        return blob_service_client, container_client
    except Exception as e:
        print(f"Error initializing Azure Blob Service or Container Client: {e}")
        raise e

def list_blobs_in_folder(folder_name):
    """
    List all blobs in a specific folder in Azure Blob Storage.

    Args:
        folder_name (str): The folder to list blobs from.

    Returns:
        dict: Dictionary where keys are dates, and values are lists of blob names for that date.
    """
    try:
        _, container_client = get_blob_service_clients()
        blobs = container_client.list_blobs(name_starts_with=f"{folder_name}/")
        grouped_blobs = {}

        for blob in blobs:
            file_name = blob.name.split("/")[-1]  # Extract the file name
            if not file_name:  # Skip empty folder paths
                continue
            parts = file_name.split("_")[:3]  # Extract the date (e.g., 2023_11_14)
            if len(parts) == 3:
                date_key = "_".join(parts)  # Format: YYYY_MM_DD
            else:
                date_key = "Unknown Date"
            grouped_blobs.setdefault(date_key, []).append(blob.name)

        return grouped_blobs
    except Exception as e:
        print(f"Error listing blobs in folder {folder_name}: {e}")
        raise e

def upload_to_azure(folder_name, file_name, file_content):
    """
    Uploads a file to a specified folder in Azure Blob Storage.

    Args:
        folder_name (str): The folder in the Azure container (e.g., raw, dirty, clean).
        file_name (str): The name of the file to upload.
        file_content (bytes): The binary content of the file to upload.

    Returns:
        str: Success message with the uploaded file path.
    """
    try:
        # Validate inputs
        if not folder_name or not file_name:
            raise ValueError("Folder name and file name cannot be empty.")
        if not file_content:
            raise ValueError("File content is empty or None.")

        # Initialize Azure Blob Service clients
        _, container_client = get_blob_service_clients()

        # Construct the blob path
        blob_name = f"{folder_name}/{file_name}"
        blob_client = container_client.get_blob_client(blob_name)

        # Upload the file, overwriting if it already exists
        blob_client.upload_blob(file_content, overwrite=True)
        print(f"Successfully uploaded {file_name} to Azure at {blob_name}.")
        return f"File successfully uploaded to: {blob_name}"
    except Exception as e:
        print(f"Error uploading {file_name} to Azure: {e}")
        raise Exception(f"Failed to upload file {file_name}: {e}")


def download_from_azure(folder_name, file_name, as_text=True):
    """
    Download a file from Azure Blob Storage.

    Args:
        folder_name (str): The folder in the Azure container (e.g., clean, dirty, raw).
        file_name (str): The name of the file to download.
        as_text (bool): Whether to decode the file content as text or return binary content.

    Returns:
        str or bytes: The content of the file as text or binary.
    """
    try:
        _, container_client = get_blob_service_clients()
        blob_name = f"{folder_name}/{file_name}"
        blob_client = container_client.get_blob_client(blob_name)
        downloader = blob_client.download_blob(max_concurrency=5)

        if as_text:
            # Read as binary first and detect encoding for text decoding
            raw_data = downloader.readall()
            detected_encoding = chardet.detect(raw_data)['encoding']
            print(f"Detected encoding: {detected_encoding}")
            return raw_data.decode(detected_encoding)  # Decode using detected encoding
        else:
            return downloader.readall()  # Return binary content if `as_text` is False

    except Exception as e:
        print(f"Error downloading blob {blob_name}: {e}")
        raise e

