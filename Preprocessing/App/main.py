# Standard Python imports
import os
import sys

# Load environment variables and set Python path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set PYTHONPATH from .env if available
python_path = os.getenv("PYTHONPATH")
if python_path:
    sys.path.append(python_path)

# Now import all other dependencies
from datetime import datetime
import streamlit as st
import weaviate  # Import Weaviate client
from preprocessing_pipeline.pdf_conversion import convert_pdf_to_text
from preprocessing_pipeline.audio_transcription import transcribe_audio
from preprocessing_pipeline.text_cleaning import clean_text
from preprocessing_pipeline.chunking_vector_embedding import process_and_embed_text  
from utils.azure_blob_utils import upload_to_azure, download_from_azure
from utils.azure_blob_utils import list_blobs_in_folder, download_from_azure

# Set up Weaviate client
client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))
)

# Generate standardized file names
def generate_file_name(metadata, stage):
    meeting_date = metadata["meeting_date"].strftime("%Y_%m_%d")
    meeting_type = "BOC" if metadata["meeting_type"] == "Board of Commissioners" else "PB"
    file_type = metadata["file_type"]
    return f"{meeting_date}_{meeting_type}_{file_type}_{stage}"

# Check and overwrite files in the local storage
def save_file_with_overwrite(file_path, content):
    if os.path.exists(file_path):
        os.remove(file_path)  # Overwrite existing file
    with open(file_path, "w") as f:
        f.write(content)

# Fetch documents from Weaviate
def fetch_uploaded_documents():
    # Query Weaviate for documents
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
    response = client.query.raw(query)
    documents = response.get("data", {}).get("Get", {}).get("Documents", [])
    return documents

# Define pages
def home_page():
    # Apply custom styling with IBM Plex Mono
    st.markdown(f"""
    <style>
    /* Main Background and Flex Layout for Cover Screen */
    .main {{
        background: #f0f2e9;
        font-family: 'IBM Plex Mono', monospace;
    }}
    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 50px;
        height: 50vh;
        flex-direction: column;
    }}
    
    /* Title Text Styling */
    .main-text {{
        font-size: 150px;
        color: #0D6051;
        opacity: 0.9;
        font-weight: 700;
        font-family: 'IBM Plex Mono', monospace;
        line-height: 1;
        text-align: center;
    }}

    /* Description Text */
    .description {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 18px;
        color: #263d36;
        text-align: center;
        margin-top: 20px;
    }}

    /* Buttons */
    .btn {{
        background-color: #0D6051;
        color: white;
        font-size: 25px;
        padding: 20px 10px;
        border-radius: 10px;
        text-align: center;
        cursor: pointer;
        border: none;
    }}

    .btn:hover {{
        background-color: #2f8479;
    }}
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="title-container">
        <h1 class="main-text">Minute Mate</h1>
        <p class="description">
            Welcome to Minute Mate; this is a staff-level application to upload meeting audios, minutes, and agendas to provide further context to the front end.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation buttons (centered)
    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Upload Files", key="upload", help="Upload meeting documents and audio files"):
            st.session_state.page = "upload"

    with col2:
        if st.button("View Documents", key="view", help="View the documents that have been uploaded"):
            st.session_state.page = "view"

# Define pages
def upload_files_page():
    st.title("Upload Municipal Meeting Documents")
    
    # Sidebar for metadata and options selection
    st.sidebar.header("Document Metadata & Transcription Options")
    meeting_date = st.sidebar.date_input("Select Meeting Date", datetime.today())
    meeting_type = st.sidebar.selectbox("Meeting Type", ["Planning Board", "Board of Commissioners"])
    file_type = st.sidebar.radio("File Type", ["Agenda", "Minutes", "Audio"])
    model_option = st.sidebar.selectbox("Select Transcription Model", ["default", "best", "nano"])
    speaker_labels = st.sidebar.checkbox("Enable Speaker Diarization")

    # Save metadata
    if st.sidebar.button("Save Metadata"):
        st.session_state["metadata"] = {
            "meeting_date": meeting_date,
            "meeting_type": meeting_type,
            "file_type": file_type,
            "model": model_option,
            "speaker_labels": speaker_labels
        }

    st.header("Upload New Document")
    file = st.file_uploader("Choose a file to upload", type=["pdf", "mp3", "wav"])

    # Initialize progress bar
    progress_bar = st.progress(0)

    if file and "metadata" in st.session_state:
        metadata = st.session_state["metadata"]
        
        # Preserve the original file extension
        file_extension = os.path.splitext(file.name)[1]
        raw_file_name = f"{generate_file_name(metadata, 'Raw')}{file_extension}"

        # Stage 1: Upload to Raw
        upload_to_azure("raw", raw_file_name, file.read())
        st.write(f"Uploaded file to Azure `raw/` folder: {raw_file_name}")
        progress_bar.progress(20)

        # Stage 2: Process based on file type
        if metadata["file_type"] == "Audio" and file_extension in [".mp3", ".wav"]:
            # Transcribe audio
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
            # Extract text from PDF
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
            cleaned_text = clean_text(dirty_file_name)  # Updated to handle chunked cleaning
        clean_file_name = generate_file_name(metadata, "Cleaned") + ".txt"
        upload_to_azure("clean", clean_file_name, cleaned_text)
        st.write(f"Uploaded cleaned text to `clean/` folder: {clean_file_name}")

        # Display cleaned text
        st.text_area("Cleaned Text:", cleaned_text, height=200)
        st.download_button("Download Cleaned Text", data=cleaned_text, file_name=clean_file_name)

        # Stage 4: Chunk and Embed into Weaviate
        with st.spinner("Chunking and embedding text into Weaviate..."):
            process_and_embed_text(clean_file_name, metadata)  # Call the combined chunking and embedding function
        st.success("Document processed and embedded successfully!")
        progress_bar.progress(100)

    # Navigation buttons (centered)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Return Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("View Documents"):
            st.session_state.page = "view"

# Define the view_documents_page function
def view_documents_page():
    st.title("Uploaded Documents")

    # Fetch files from the Azure Blob Storage
    try:
        # List blobs in the 'raw', 'dirty', and 'clean' folders
        raw_blobs = list_blobs_in_folder("raw")
        dirty_blobs = list_blobs_in_folder("dirty")
        clean_blobs = list_blobs_in_folder("clean")

        # Display documents from 'raw' folder
        if raw_blobs:
            st.subheader("Raw Documents")
            for blob in raw_blobs:
                st.write(f"- {blob}")
                if st.button(f"Download {blob}", key=f"download_raw_{blob}"):
                    file_content = download_from_azure("raw", blob)
                    st.download_button("Download", data=file_content, file_name=blob)

        # Display documents from 'dirty' folder
        if dirty_blobs:
            st.subheader("Dirty Documents")
            for blob in dirty_blobs:
                st.write(f"- {blob}")
                if st.button(f"Download {blob}", key=f"download_dirty_{blob}"):
                    file_content = download_from_azure("dirty", blob)
                    st.download_button("Download", data=file_content, file_name=blob)

        # Display documents from 'clean' folder
        if clean_blobs:
            st.subheader("Clean Documents")
            for blob in clean_blobs:
                st.write(f"- {blob}")
                if st.button(f"Download {blob}", key=f"download_clean_{blob}"):
                    file_content = download_from_azure("clean", blob)
                    st.download_button("Download", data=file_content, file_name=blob)

        # If no files are found in any folder
        if not raw_blobs and not dirty_blobs and not clean_blobs:
            st.write("No documents found in the Azure Blob Storage.")

    except Exception as e:
            st.error(f"Error fetching documents from Azure Blob Storage: {e}")
                                                      
    # Navigation buttons (centered)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Return Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("Upload Files"):
            st.session_state.page = "upload"


# Main page selection
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "upload":
    upload_files_page()
elif st.session_state.page == "view":
    view_documents_page()
