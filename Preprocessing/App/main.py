# Standard Python imports
import sys
import os
from pathlib import Path
from datetime import datetime

# Dynamically add the parent directory to PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import dependencies
import streamlit as st
import weaviate  # Import Weaviate client
from azure.storage.blob import BlobServiceClient
from preprocessing_pipeline.pdf_conversion import convert_pdf_to_text
from preprocessing_pipeline.audio_transcription import transcribe_audio
from preprocessing_pipeline.text_cleaning import clean_text
from preprocessing_pipeline.chunking_vector_embedding import (
    tokenize_and_embed_text,
    fetch_matching_chunks,
    delete_matching_chunks
)
from utils.azure_blob_utils import (
    upload_to_azure,
    download_from_azure,
    list_blobs_in_folder,
    get_blob_service_clients,  # Use this standardized function
)

# Helper function: Initialize Weaviate client
def get_weaviate_client():
    api_keys = st.session_state.get("api_keys", {})
    weaviate_url = api_keys.get("WEAVIATE_URL")
    weaviate_api_key = api_keys.get("WEAVIATE_API_KEY")

    if not weaviate_url or not weaviate_api_key:
        st.error("Weaviate API configuration is missing. Please set it on the Home Page.")
        return None

    return weaviate.Client(
        url=weaviate_url,
        auth_client_secret=weaviate.AuthApiKey(api_key=weaviate_api_key)
)

# Helper function: Validate API Keys
def are_api_keys_set():
    """
    Validates that all required API keys are present and non-empty in the session state.
    """
    required_keys = [
        "OPENAI_API_KEY",
        "WEAVIATE_URL",
        "WEAVIATE_API_KEY",
        "ASSEMBLY_AI_KEY",
        "AZURE_STORAGE_CONNECTION_STRING",
        "AZURE_STORAGE_CONTAINER"
    ]
    return all(
        key in st.session_state.get("api_keys", {}) and st.session_state["api_keys"][key]
        for key in required_keys
    )

# Initialize clients dynamically
client = None

# Helper function: Generate standardized file names
def generate_file_name(metadata, stage):
    meeting_date = metadata["meeting_date"].strftime("%Y_%m_%d")
    meeting_type = "BOC" if metadata["meeting_type"] == "Board of Commissioners" else "PB"
    file_type = metadata["file_type"]
    return f"{meeting_date}_{meeting_type}_{file_type}_{stage}"

# Helper function: Check and overwrite files in local storage
def save_file_with_overwrite(file_path, content):
    if os.path.exists(file_path):
        os.remove(file_path)  # Overwrite existing file
    with open(file_path, "w") as f:
        f.write(content)

# Helper function: Fetch documents from Weaviate
def fetch_uploaded_documents():
    """
    Fetches documents stored in Weaviate.
    Returns:
        list: List of uploaded documents with metadata.
    """
    client = get_weaviate_client()
    if not client:
        st.error("Weaviate client is not initialized. Please configure API keys.")
        return []

    query = """
    {
      Get {
        Documents {
          file_name
          file_type
          meeting_date
          meeting_type
          clean_text
          chunks
        }
      }
    }
    """
    try:
        response = client.query.raw(query)
        documents = response.get("data", {}).get("Get", {}).get("Documents", [])
        return documents
    except Exception as e:
        st.error(f"Error fetching documents from Weaviate: {e}")
        return []

# Home Page
def home_page():
    # Custom styling for the homepage
    st.markdown("""
    <style>
    .main {
        background: #f0f2e9;
        font-family: 'IBM Plex Mono', monospace;
    }
    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 50px;
        height: 50vh;
        flex-direction: column;
    }
    .main-text {
        font-size: 150px;
        color: #0D6051;
        opacity: 0.9;
        font-weight: 700;
        font-family: 'IBM Plex Mono', monospace;
        line-height: 1;
        text-align: center;
    }
    .description {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 18px;
        color: #263d36;
        text-align: center;
        margin-top: 20px;
    }
    .stButton>button {
        background-color: #0D6051;
        color: white;
        font-size: 25px;
        font-weight: bold;
        padding: 15px 30px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #2f8479;
    }
    a {
        color: #0D6051;
        text-decoration: none;
        font-weight: bold;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="title-container">
        <h1 class="main-text">Minute Mate</h1>
        <p class="description">
            Welcome to Minute Mate! Use the sidebar to configure your API keys and get started. 
            Once configured, navigate using the buttons below to upload files or view documents.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for API Key Configuration and Instructions
    st.sidebar.header("Setup")

    # Collapsible section for API Key Configuration
    with st.sidebar.expander("API Key Configuration", expanded=True):
        st.subheader("Submit Your API Keys")
        with st.form(key="api_key_form"):
            # OpenAI Keys
            openai_api_key = st.text_input("OpenAI API Key", type="password")
            openai_base_url = st.text_input("OpenAI Base URL", value="https://api.openai.com/v1")

            # Weaviate Keys
            weaviate_url = st.text_input("Weaviate URL", type="password")
            weaviate_api_key = st.text_input("Weaviate API Key", type="password")

            # AssemblyAI Key
            assembly_ai_key = st.text_input("AssemblyAI API Key", type="password")

            # Azure Keys
            azure_connection_string = st.text_area("Azure Storage Connection String")
            azure_container_name = st.text_input("Azure Storage Container Name", type="password")

            submit_button = st.form_submit_button("Save API Keys")

            if submit_button:
                st.session_state["api_keys"] = {
                    "OPENAI_API_KEY": openai_api_key,
                    "OPENAI_BASE_URL": openai_base_url,
                    "WEAVIATE_URL": weaviate_url,
                    "WEAVIATE_API_KEY": weaviate_api_key,
                    "ASSEMBLY_AI_KEY": assembly_ai_key,
                    "AZURE_STORAGE_CONNECTION_STRING": azure_connection_string,
                    "AZURE_STORAGE_CONTAINER": azure_container_name
                }
                st.success("API Keys saved successfully!")
                st.rerun()

    # Collapsible section for How to Get API Keys
    with st.sidebar.expander("How to Get API Keys", expanded=False):
        st.subheader("API Key Setup Instructions")
        st.markdown("""
        - **OpenAI**  
          - [Get your OpenAI API Key](https://platform.openai.com/account/api-keys)  
          - Set `OPENAI_API_KEY` in the sidebar.  
          - For `OPENAI_BASE_URL`, use `https://api.openai.com/v1` or leave it blank.

        - **Weaviate**  
          - [Access your Weaviate Cluster details](https://console.weaviate.cloud/cluster-details)  
          - Follow [this guide](https://weaviate.io/developers/wcs/create-instance) to create a new cluster if needed.  
          - Set `WEAVIATE_URL` with the REST endpoint and `WEAVIATE_API_KEY` with the admin key.

        - **AssemblyAI**  
          - [Create an AssemblyAI account](https://www.assemblyai.com/app)  
          - Copy your API key from the homepage and set it in `ASSEMBLY_AI_KEY`.

        - **Azure**  
          - [Create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal)  
          - Go to the Access Keys section in Azure and copy the connection string into `AZURE_STORAGE_CONNECTION_STRING`.  
          - Specify the container name in `AZURE_STORAGE_CONTAINER_NAME`.
        """)

    # Navigation Buttons with Validation
    col1, col2 = st.columns([1, 1])
    if are_api_keys_set():
        try:
            client = get_weaviate_client()
            blob_service_client, container_client = get_blob_service_clients()

            # Validate connections
            if not client:
                st.error("Failed to connect to Weaviate. Please check your API configuration.")
                return
            if not blob_service_client or not container_client:
                st.error("Failed to connect to Azure Blob Storage. Please check your API configuration.")
                return

            with col1:
                if st.button("Upload Files", key="upload", help="Upload meeting documents and audio files"):
                    st.session_state.page = "upload"
            with col2:
                if st.button("View Documents", key="view", help="View the documents that have been uploaded"):
                    st.session_state.page = "view"

        except Exception as e:
            st.error(f"Error validating API keys: {e}")
    else:
        st.warning("API Keys must be configured to access other pages.")
        with col1:
            st.button("Upload Files", key="upload_disabled", disabled=True)
        with col2:
            st.button("View Documents", key="view_disabled", disabled=True)

def upload_files_page():
    st.title("Upload Municipal Meeting Documents")

    # Sidebar Configuration
    st.sidebar.header("Upload File Configuration")

    # Collapsible section for Document Metadata and Transcription Options
    with st.sidebar.expander("Document Metadata & Transcription Options", expanded=True):
        st.subheader("Document Metadata")
        meeting_date = st.date_input("Select Meeting Date", datetime.today())
        meeting_type = st.selectbox("Meeting Type", ["Planning Board", "Board of Commissioners"])
        file_type = st.radio("File Type", ["Agenda", "Minutes", "Audio"])
        model_option = st.selectbox("Select Transcription Model", ["default", "best", "nano"])
        speaker_labels = st.checkbox("Enable Speaker Diarization")

        # Save metadata into session state
        if st.button("Save Metadata", key="save_metadata"):
            st.session_state["metadata"] = {
                "meeting_date": meeting_date,
                "meeting_type": meeting_type,
                "file_type": file_type,
                "model": model_option,
                "speaker_labels": speaker_labels
            }
            st.success("Metadata saved successfully!")

    # Collapsible section to display Saved API Keys
    with st.sidebar.expander("Saved API Keys", expanded=False):
        st.subheader("API Keys in Use")
        if "api_keys" in st.session_state:
            api_keys = st.session_state["api_keys"]
            st.markdown(f"""
            - **OpenAI API Key**: {api_keys.get("OPENAI_API_KEY", "Not Set")}
            - **OpenAI Base URL**: {api_keys.get("OPENAI_BASE_URL", "Not Set")}
            - **Weaviate URL**: {api_keys.get("WEAVIATE_URL", "Not Set")}
            - **Weaviate API Key**: {api_keys.get("WEAVIATE_API_KEY", "Not Set")}
            - **AssemblyAI API Key**: {api_keys.get("ASSEMBLY_AI_KEY", "Not Set")}
            - **Azure Connection String**: {api_keys.get("AZURE_STORAGE_CONNECTION_STRING", "Not Set")}
            - **Azure Container Name**: {api_keys.get("AZURE_STORAGE_CONTAINER", "Not Set")}
            """)
        else:
            st.warning("No API keys found. Please configure them on the Home Page.")

    # Initialize Azure Blob Storage and Weaviate clients
    try:
        blob_service_client, container_client = get_blob_service_clients()
        weaviate_client = get_weaviate_client()

        if not blob_service_client or not container_client or not weaviate_client:
            st.error("API key configurations are incomplete. Please configure all keys on the Home Page.")
            return

    except Exception as e:
        st.error(f"Error initializing clients: {e}")
        return

    # Main Upload Section
    st.header("Upload New Document")
    file = st.file_uploader("Choose a file to upload", type=["pdf", "mp3", "wav"])

    # Initialize progress bar
    progress_bar = st.progress(0)

    # Handle file upload
    if file and "metadata" in st.session_state:
        metadata = st.session_state["metadata"]

        # Preserve the original file extension
        file_extension = os.path.splitext(file.name)[1]
        raw_file_name = f"{generate_file_name(metadata, 'Raw')}{file_extension}"

        try:
            # Upload the file to Azure Blob Storage
            upload_to_azure("raw", raw_file_name, file.read())
            st.write(f"Uploaded file to Azure `raw/` folder: {raw_file_name}")
            progress_bar.progress(20)

            # Stage 2: Process based on file type
            if metadata["file_type"] == "Audio" and file_extension in [".mp3", ".wav"]:
                with st.spinner(f"Transcribing audio using {metadata['model']} model..."):
                    transcribed_text = transcribe_audio(
                        raw_file_name=raw_file_name,
                        model=metadata["model"],
                        speaker_labels=metadata["speaker_labels"]
                    )
                if transcribed_text:
                    dirty_file_name = generate_file_name(metadata, "Transcription") + ".txt"
                    upload_to_azure("dirty", dirty_file_name, transcribed_text)
                    st.write(f"Uploaded transcription to `dirty/` folder: {dirty_file_name}")
                    st.text_area("Transcribed Audio Text:", transcribed_text, height=200)
                    st.download_button("Download Transcribed Text", data=transcribed_text, file_name=dirty_file_name)
                else:
                    st.error("Failed to transcribe the audio.")

            elif metadata["file_type"] in ["Agenda", "Minutes"] and file_extension == ".pdf":
                with st.spinner("Extracting text from PDF..."):
                    extracted_text = convert_pdf_to_text(raw_file_name)
                if extracted_text:
                    dirty_file_name = generate_file_name(metadata, "TextExtraction") + ".txt"
                    upload_to_azure("dirty", dirty_file_name, extracted_text)
                    st.write(f"Uploaded extracted text to `dirty/` folder: {dirty_file_name}")
                    st.text_area("Extracted PDF Text:", extracted_text, height=200)
                    st.download_button("Download Extracted Text", data=extracted_text, file_name=dirty_file_name)
                else:
                    st.error("Failed to extract text from the PDF.")

            # Stage 3: Clean Text and Upload to Clean
            dirty_content = download_from_azure("dirty", dirty_file_name)
            with st.spinner("Cleaning text using generative AI..."):
                cleaned_text = clean_text(dirty_file_name)  # Pass the actual content
            clean_file_name = generate_file_name(metadata, "Cleaned") + ".txt"
            upload_to_azure("clean", clean_file_name, cleaned_text)
            st.write(f"Uploaded cleaned text to `clean/` folder: {clean_file_name}")

            # Stage 4: Check and Delete Existing Embeddings
            with st.spinner("Checking for existing embeddings in Weaviate..."):
                matching_chunks = fetch_matching_chunks(
                    str(metadata["meeting_date"]),
                    metadata["meeting_type"],
                    metadata["file_type"],
                    clean_file_name
                )
                if matching_chunks:
                    st.write(f"Found {len(matching_chunks)} existing chunks. Deleting...")
                    delete_matching_chunks(matching_chunks)
                else:
                    st.write("No existing chunks found.")

            # Stage 5: Chunk and Embed into Weaviate
            with st.spinner("Chunking and embedding text into Weaviate..."):
                tokenize_and_embed_text(clean_file_name, metadata)
            st.success("Document processed and embedded successfully!")
            progress_bar.progress(100)

        except Exception as e:
            st.error(f"Error processing file: {e}")

    # Navigation buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Return Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("View Documents"):
            st.session_state.page = "view"


def view_documents_page():
    st.title("View Uploaded Files")

    # Sidebar Configuration
    st.sidebar.header("View Documents Configuration")

    # Collapsible section to display Saved API Keys
    with st.sidebar.expander("Saved API Keys", expanded=False):
        st.subheader("API Keys in Use")
        if "api_keys" in st.session_state:
            api_keys = st.session_state["api_keys"]
            st.markdown(f"""
            - **OpenAI API Key**: {api_keys.get("OPENAI_API_KEY", "Not Set")}
            - **OpenAI Base URL**: {api_keys.get("OPENAI_BASE_URL", "Not Set")}
            - **Weaviate URL**: {api_keys.get("WEAVIATE_URL", "Not Set")}
            - **Weaviate API Key**: {api_keys.get("WEAVIATE_API_KEY", "Not Set")}
            - **AssemblyAI API Key**: {api_keys.get("ASSEMBLY_AI_KEY", "Not Set")}
            - **Azure Connection String**: {api_keys.get("AZURE_STORAGE_CONNECTION_STRING", "Not Set")}
            - **Azure Container Name**: {api_keys.get("AZURE_STORAGE_CONTAINER", "Not Set")}
            """)
        else:
            st.warning("No API keys found. Please configure them on the Home Page.")

    # Fetch files and group them by folder and date
    try:
        raw_files = list_blobs_in_folder("raw")
        dirty_files = list_blobs_in_folder("dirty")
        clean_files = list_blobs_in_folder("clean")

        def display_grouped_files(folder_name, grouped_files):
            """
            Display grouped files by date for a specific folder.

            Args:
                folder_name (str): The name of the folder (raw, dirty, clean).
                grouped_files (dict): Dictionary of grouped files by date.
            """
            with st.expander(f"{folder_name.capitalize()} Files", expanded=False):
                for date, files in grouped_files.items():
                    st.markdown(f"**Date: {date}**")
                    for file_path in files:
                        file_name = file_path.split("/")[-1]
                        if st.button(f"Download {file_name}", key=f"{folder_name}_{file_name}_button"):
                            try:
                                file_content = download_from_azure(folder_name, file_name)
                                st.download_button(
                                    label=f"Download {file_name}",
                                    data=file_content,
                                    file_name=file_name,
                                    key=f"download_{folder_name}_{file_name}"
                                )
                            except Exception as e:
                                st.error(f"Error downloading {file_name}: {e}")

        # Display files for each folder
        display_grouped_files("clean", clean_files)
        display_grouped_files("dirty", dirty_files)
        display_grouped_files("raw", raw_files)

    except Exception as e:
        st.error(f"Error fetching files from Azure Blob Storage: {e}")

    # Navigation Buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Return Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("Upload Files"):
            st.session_state.page = "upload"

# Main page selection logic
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "upload":
    upload_files_page()
elif st.session_state.page == "view":
    view_documents_page()
