import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env
load_dotenv()

# Set PYTHONPATH from .env if available
python_path = os.getenv("PYTHONPATH")
if python_path:
    sys.path.append(python_path)


import streamlit as st
import weaviate  # Import Weaviate client
from preprocessing_pipeline.pdf_conversion import convert_pdf_to_text
from preprocessing_pipeline.audio_transcription import transcribe_audio
from preprocessing_pipeline.text_cleaning import clean_text
from preprocessing_pipeline.chunking_tokenization import process_text_chunks
from preprocessing_pipeline.vector_embedding import embed_text

# Set up Weaviate client
client = weaviate.Client(
    url=os.getenv("WEAVIATE_URL"),
    auth_client_secret=weaviate.AuthApiKey(api_key=os.getenv("WEAVIATE_API_KEY"))
)

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

def upload_files_page():
    st.title("Upload Municipal Meeting Documents")
    
    # Sidebar for metadata and options selection
    st.sidebar.header("Document Metadata & Transcription Options")

    # Metadata Input Fields
    meeting_date = st.sidebar.date_input("Select Meeting Date", datetime.today())
    meeting_type = st.sidebar.selectbox("Meeting Type", ["Planning Board", "Board of Commissioners"])
    file_type = st.sidebar.radio("File Type", ["Agenda", "Minutes", "Audio"])

    # Transcription Model and Language Options
    model_option = st.sidebar.selectbox("Select Transcription Model", ["default", "best", "nano"])
    speaker_labels = st.sidebar.checkbox("Enable Speaker Diarization")

    # Save Metadata Button
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
        progress_bar.progress(10)
        st.write("Stage: Metadata Saved")

        if metadata["file_type"] in ["Agenda", "Minutes"] and file.type == "application/pdf":
            # Stage: PDF to Dirty Text Conversion
            with st.spinner("Converting PDF to text..."):
                dirty_text = convert_pdf_to_text(file)
            
            pdf_text_path = "pdf_text_output.txt"
            with open(pdf_text_path, "w") as f:
                f.write(dirty_text)
            
            progress_bar.progress(30)
            st.write("Stage: PDF Conversion Complete")
            
            # Display and download PDF text conversion
            st.text_area("Converted PDF Text:", dirty_text, height=200)
            st.download_button("Download PDF Text", data=dirty_text, file_name=pdf_text_path)

        elif metadata["file_type"] == "Audio" and file.type in ["audio/mpeg", "audio/wav"]:
            # Stage: Audio Transcription with selected model and speaker labels
            with st.spinner(f"Transcribing audio using {metadata['model']} model..."):
                dirty_text = transcribe_audio(file, model=metadata["model"], speaker_labels=metadata["speaker_labels"])
            
            transcription_path = "transcription_output.txt"
            with open(transcription_path, "w") as f:
                f.write(dirty_text)
            
            progress_bar.progress(30)
            st.write("Stage: Audio Transcription Complete")
            
            # Display and download transcription
            st.text_area("Audio Transcription:", dirty_text, height=200)
            st.download_button("Download Transcription", data=dirty_text, file_name=transcription_path)

        # Continue processing if dirty_text was successfully created
        if dirty_text:
            # Stage: Text Cleaning
            with st.spinner("Cleaning text with generative AI..."):
                partly_clean_text = clean_text(dirty_text)
            
            cleaned_text_path = "cleaned_text_output.txt"
            with open(cleaned_text_path, "w") as f:
                f.write(partly_clean_text)
            
            progress_bar.progress(60)
            st.write("Stage: Text Cleaning Complete")
            
            # Display and download cleaned text
            st.text_area("Cleaned Text:", partly_clean_text, height=200)
            st.download_button("Download Cleaned Text", data=partly_clean_text, file_name=cleaned_text_path)

            # Stage: Chunking and Tokenization
            with st.spinner("Chunking and tokenizing text..."):
                text_chunks = process_text_chunks(partly_clean_text)
            progress_bar.progress(80)
            st.write("Stage: Chunking and Tokenization Complete")

            # Stage: Embedding and Storage
            with st.spinner("Embedding and storing in Weaviate..."):
                embed_text(text_chunks, metadata)
            progress_bar.progress(100)
            st.write("Stage: Embedding and Storage Complete")

            st.success("Document processed and embedded with metadata!")
        else:
            st.error("Failed to process the document.")

    # Navigation buttons (centered)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Return Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("View Documents"):
            st.session_state.page = "view"

def view_documents_page():
    st.title("Uploaded Documents")

    # Retrieve Weaviate URL and API Key from environment variables
    weaviate_url = os.getenv("WEAVIATE_URL")
    weaviate_api_key = os.getenv("WEAVIATE_API_KEY")

    if not weaviate_url or not weaviate_api_key:
        st.error("Weaviate connection details (URL or API Key) are missing.")
        return

    # Initialize Weaviate client with API key for authentication
    client = weaviate.Client(
        url=weaviate_url,
        auth_client_secret=weaviate_api_key
    )

    # Fetch all objects from Weaviate
    try:
        # Get all objects from the collection (assuming "Documents" is the name of your collection)
        result = client.data_object.get(class_name="Documents", properties=["file_name", "file_type", "meeting_date", "meeting_type", "clean_text", "chunks"])

        if result['objects']:
            for item in result['objects']:
                file_name = item['properties'].get('file_name', 'N/A')
                file_type = item['properties'].get('file_type', 'N/A')
                meeting_date = item['properties'].get('meeting_date', 'N/A')
                meeting_type = item['properties'].get('meeting_type', 'N/A')
                clean_text = item['properties'].get('clean_text', 'No clean text available')
                chunks = item['properties'].get('chunks', 'No chunks available')

                # Display the document details in Streamlit
                st.subheader(f"Document: {file_name}")
                st.write(f"**File Type:** {file_type}")
                st.write(f"**Meeting Date:** {meeting_date}")
                st.write(f"**Meeting Type:** {meeting_type}")
                st.write(f"**Clean Text:** {clean_text[:300]}...")  # Show a preview of the clean text
                st.write(f"**Chunks:** {chunks[:300]}...")  # Show a preview of the chunks
                st.write("---")
        else:
            st.write("No documents found in the Weaviate database.")
    except Exception as e:
        st.error(f"Error fetching documents from Weaviate: {e}")

    # Navigation buttons (centered)
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Return Home"):
            st.session_state.page = "home"
    with col2:
        if st.button("Upload Files"):
            st.session_state.page = "upload"
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
