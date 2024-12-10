#This is a few different pytests!

import os
import sys
import importlib
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the parent directory (Preprocessing) to the Python module search path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

def test_dependencies_installed():
    dependencies = [
        "streamlit", "requests", "azure.storage.blob", "openai", "weaviate",
        "fitz", "assemblyai", "transformers", "chardet", "pytest", "easyocr", "os", "sys", "importlib"
    ]
    for lib in dependencies:
        assert importlib.util.find_spec(lib) is not None, f"{lib} is not installed!"

def test_env_variables():
    required_vars = [
        "OPENAI_API_KEY", "OPENAI_BASE_URL", "WEAVIATE_URL", "WEAVIATE_API_KEY",
        "ASSEMBLY_AI_KEY", "AZURE_STORAGE_CONNECTION_STRING", "AZURE_STORAGE_CONTAINER", "PYTHONPATH"
    ]

    # Debugging
    for var in required_vars:
        print(f"{var}: {os.getenv(var)}")

    missing_or_empty_vars = [
        var for var in required_vars if not os.getenv(var) or os.getenv(var).strip() == ""
    ]
    assert not missing_or_empty_vars, f"Missing or empty variables: {', '.join(missing_or_empty_vars)}"

from utils.azure_blob_utils import download_from_azure
def test_download_from_azure():
    """
    Test downloading a specific file from Azure Blob Storage.
    """
    # File details
    folder_name = "raw"
    file_name = "2023_08_01_BOC_Agenda_Raw.pdf"
    downloaded_file_path = "downloaded_2023_08_01_BOC_Agenda_Raw.pdf"
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    # Ensure container name is loaded from environment
    assert container_name, "AZURE_STORAGE_CONTAINER is not set in the .env file."

    print(f"Attempting to download {folder_name}/{file_name} from Azure Blob Storage...")

    # Download the file
    try:
        content = download_from_azure(folder_name, file_name, as_text=False)
        # Save the downloaded content locally
        with open(downloaded_file_path, "wb") as file:
            file.write(content)

        # Check if the file exists locally
        assert os.path.exists(downloaded_file_path), f"Downloaded file {downloaded_file_path} does not exist!"
        print(f"Download successful. File saved to {downloaded_file_path}.")
    except Exception as e:
        assert False, f"Download failed with error: {e}"

    # Cleanup: Remove the downloaded file after the test
    try:
        if os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)
            print(f"Cleaned up: {downloaded_file_path}.")
    except Exception as cleanup_error:
        print(f"Error during cleanup: {cleanup_error}")

def test_download_from_dirty():
    """
    Test downloading a specific file from the 'dirty' folder in Azure Blob Storage.
    """
    # File details
    folder_name = "dirty"
    file_name = "2023_08_01_BOC_Agenda_TextExtraction.txt"
    downloaded_file_path = "downloaded_2023_08_01_BOC_Agenda_TextExtraction.txt"
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    # Ensure container name is loaded from environment
    assert container_name, "AZURE_STORAGE_CONTAINER is not set in the .env file."

    print(f"Attempting to download {folder_name}/{file_name} from Azure Blob Storage...")

    # Download the file
    try:
        content = download_from_azure(folder_name, file_name, as_text=True)
        # Save the downloaded content locally
        with open(downloaded_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Check if the file exists locally
        assert os.path.exists(downloaded_file_path), f"Downloaded file {downloaded_file_path} does not exist!"
        print(f"Download successful. File saved to {downloaded_file_path}.")
    except Exception as e:
        assert False, f"Download failed with error: {e}"

    # Cleanup: Remove the downloaded file after the test
    try:
        if os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)
            print(f"Cleaned up: {downloaded_file_path}.")
    except Exception as cleanup_error:
        print(f"Error during cleanup: {cleanup_error}")


def test_download_from_clean():
    """
    Test downloading a specific file from the 'clean' folder in Azure Blob Storage.
    """
    # File details
    folder_name = "clean"
    file_name = "2023_08_01_BOC_Agenda_Cleaned.txt"
    downloaded_file_path = "downloaded_2023_08_01_BOC_Agenda_Cleaned.txt"
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    # Ensure container name is loaded from environment
    assert container_name, "AZURE_STORAGE_CONTAINER is not set in the .env file."

    print(f"Attempting to download {folder_name}/{file_name} from Azure Blob Storage...")

    # Download the file
    try:
        content = download_from_azure(folder_name, file_name, as_text=True)
        # Save the downloaded content locally
        with open(downloaded_file_path, "w", encoding="utf-8") as file:
            file.write(content)

        # Check if the file exists locally
        assert os.path.exists(downloaded_file_path), f"Downloaded file {downloaded_file_path} does not exist!"
        print(f"Download successful. File saved to {downloaded_file_path}.")
    except Exception as e:
        assert False, f"Download failed with error: {e}"

    # Cleanup: Remove the downloaded file after the test
    try:
        if os.path.exists(downloaded_file_path):
            os.remove(downloaded_file_path)
            print(f"Cleaned up: {downloaded_file_path}.")
    except Exception as cleanup_error:
        print(f"Error during cleanup: {cleanup_error}")
    
from utils.azure_blob_utils import upload_to_azure

def test_upload_to_raw():
    """
    Test uploading a file to the 'raw' folder in Azure Blob Storage.
    """
    # File details
    folder_name = "raw"
    file_name = "Test_Minutes.pdf"
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    # Ensure container name is loaded from environment
    assert container_name, "AZURE_STORAGE_CONTAINER is not set in the .env file."

    # Read the local file
    local_file_path = "Test_Minutes.pdf"  # Replace with your actual test file path
    assert os.path.exists(local_file_path), f"Local file {local_file_path} does not exist!"
    with open(local_file_path, "rb") as f:
        file_content = f.read()

    # Upload to Azure
    print(f"Uploading {local_file_path} to {folder_name}/{file_name} in Azure Blob Storage...")
    try:
        upload_to_azure(folder_name, file_name, file_content)
        print(f"Upload successful: {folder_name}/{file_name}")
    except Exception as e:
        assert False, f"Upload failed with error: {e}"


def test_upload_to_dirty():
    """
    Test uploading a file to the 'dirty' folder in Azure Blob Storage.
    """
    # File details
    folder_name = "dirty"
    file_name = "Test_Minutes.pdf"
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    # Ensure container name is loaded from environment
    assert container_name, "AZURE_STORAGE_CONTAINER is not set in the .env file."

    # Read the local file
    local_file_path = "Test_Minutes.pdf"  # Replace with your actual test file path
    assert os.path.exists(local_file_path), f"Local file {local_file_path} does not exist!"
    with open(local_file_path, "rb") as f:
        file_content = f.read()

    # Upload to Azure
    print(f"Uploading {local_file_path} to {folder_name}/{file_name} in Azure Blob Storage...")
    try:
        upload_to_azure(folder_name, file_name, file_content)
        print(f"Upload successful: {folder_name}/{file_name}")
    except Exception as e:
        assert False, f"Upload failed with error: {e}"


def test_upload_to_clean():
    """
    Test uploading a file to the 'clean' folder in Azure Blob Storage.
    """
    # File details
    folder_name = "clean"
    file_name = "Test_Minutes.pdf"
    container_name = os.getenv("AZURE_STORAGE_CONTAINER")

    # Ensure container name is loaded from environment
    assert container_name, "AZURE_STORAGE_CONTAINER is not set in the .env file."

    # Read the local file
    local_file_path = "Test_Minutes.pdf"  # Replace with your actual test file path
    assert os.path.exists(local_file_path), f"Local file {local_file_path} does not exist!"
    with open(local_file_path, "rb") as f:
        file_content = f.read()

    # Upload to Azure
    print(f"Uploading {local_file_path} to {folder_name}/{file_name} in Azure Blob Storage...")
    try:
        upload_to_azure(folder_name, file_name, file_content)
        print(f"Upload successful: {folder_name}/{file_name}")
    except Exception as e:
        assert False, f"Upload failed with error: {e}"


from preprocessing_pipeline.pdf_conversion import convert_pdf_to_text

def test_pdf_conversion():
    """
    Test the PDF to text conversion function.
    """
    # Define the test file
    test_pdf_path = "Test_Minutes.pdf"  # Replace with your test PDF file path

    # Ensure the test file exists locally
    assert os.path.exists(test_pdf_path), f"Test PDF file {test_pdf_path} does not exist!"

    # Attempt to convert the PDF to text
    try:
        print(f"Converting {test_pdf_path} to text...")
        extracted_text = convert_pdf_to_text(test_pdf_path)

        # Assertions to verify the conversion worked
        assert isinstance(extracted_text, str), "Extracted text is not a string!"
        assert len(extracted_text) > 0, "Extracted text is empty!"
        print(f"PDF conversion successful. Extracted text length: {len(extracted_text)} characters.")
    except Exception as e:
        assert False, f"PDF conversion failed with error: {e}"