# app.py
import streamlit as st
from handler import transcribe_with_whisper, diarize_audio

# Load SVG content from the file in the same directory
with open("Audio-Text/Temp Logo.svg", "r") as svg_file:
    svg_content = svg_file.read()

# Set page configuration
st.set_page_config(page_title="Minute Mate", layout="centered", initial_sidebar_state="expanded")

# Custom CSS for styling
st.markdown(f"""
    <style>
    /* Main Background Gradient */
    .main {{
        background: linear-gradient(to bottom, #f0f2e9, #ffffff);
    }}
    .title-text {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 70px;
        font-weight: bold;
        color: #0d6051;
        text-align: center;
        line-height: 1;
        margin-bottom: 20px;
    }}
    .title-text span {{
        display: block;
    }}

    /* SVG Icon Styling */
    .svg-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        width: 200px;  /* Adjust size as needed */
        height: 200px;  /* Adjust size as needed */
        opacity: 1;
        margin-bottom: 20px;
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] > div:first-child {{
        background: linear-gradient(to bottom left, #165448, #6bb2a4);
        padding: 20px;
        display: flex;
        flex-direction: column;
        height: 100%;
    }}
    .sidebar-title {{
        color: #d8b64d;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 34px;
        font-weight: bold;
        text-align: center;
    }}
    .sidebar-text {{
        color: white;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 16px;
        margin-bottom: auto;  /* Pushes the acknowledgment text to the bottom */
    }}
    .sidebar-acknowledgment {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 18px;
        color: rgba(255, 255, 255, 1);
        text-align: center;
        margin-top: 500px;
    }}

    /* Description Text */
    .description {{
        font-family: 'IBM Plex Mono', monospace;
        font-size: 18px;
        color: #263d36;
        text-align: center;
        margin: 20px 0;
    }}

    /* Drop Files Section */
    .upload-container {{
        margin-top: 30px;
        text-align: center;
    }}
    </style>
    """, unsafe_allow_html=True)

# Sidebar content with custom font size
st.sidebar.markdown("""
    <h3 class="sidebar-title" style="font-size: 30px;">About Minute Mate</h3>
""", unsafe_allow_html=True)

st.sidebar.markdown(
    """
    <div class="sidebar-text">
        Minute Mate is an interactive LLM tool that simplifies meeting transcription and summarization for town staff. 
        By uploading audio into a Streamlit app, staff can transcribe and summarize meetings, with the content stored 
        in a searchable knowledge base. The public can access this information through a prompt-based UI, enabling 
        questions about town meetings and decisions.
    </div>
    """, unsafe_allow_html=True
)

# Acknowledgment text with LinkedIn links at the bottom of the sidebar
st.sidebar.markdown("""
    <div class="sidebar-acknowledgment">
        BY 
        <a href="https://www.linkedin.com/in/abolikasar/" target="_blank" style="color: rgba(255, 255, 255, 1); text-decoration: underline;">ABOLI KASAR</a> 
        <a href="https://www.linkedin.com/in/nealdlogan/" target="_blank" style="color: rgba(255, 255, 255, 1); text-decoration: underline;">NEAL LOGAN</a> 
        <a href="https://www.linkedin.com/in/riley-leprell/" target="_blank" style="color: rgba(255, 255, 255, 1); text-decoration: underline;">RILEY LEPRELL</a> 
        <a href="https://www.linkedin.com/in/iamyashpradhan/" target="_blank" style="color: rgba(255, 255, 255, 1); text-decoration: underline;">YASH PRADHAN</a>
    </div>
""", unsafe_allow_html=True)

# SVG Icon
st.markdown("""
<div class="svg-container">
    {svg_content}
</div>
""", unsafe_allow_html=True)

# Title Text
st.markdown("""
<div class="title-text">
    <span>MINUTE</span>
    <span>MATE</span>
</div>
""", unsafe_allow_html=True)

# Description Text
st.markdown("""
<div class="description">
    To start the transcription process, upload your audio file below. This first step in the LLM pipeline will convert your audio into text, which will then be processed further in the pipeline for you. Please note that uploading large files may take some time. For the best experience, we recommend uploading audio files overnight to ensure smooth processing without interruptions.
</div>
""", unsafe_allow_html=True)


# File Upload
st.markdown('<div class="upload-container">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Drop your audio file here", type=["wav", "mp3", "m4a"], key="upload")
st.markdown('</div>', unsafe_allow_html=True)

# Audio Player and Transcription / Diarization Functions
if uploaded_file is not None:
    st.audio(uploaded_file)

    # Transcription step
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            transcription_data = transcribe_with_whisper(uploaded_file)

            if transcription_data:  # Check if transcription data is valid
                # Build the HTML for transcription display
                transcription_html = f"<div style='text-align: center; font-family: IBM Plex Mono, monospace;'>{'<br>'.join(transcription_data)}</div>"
                st.markdown(transcription_html, unsafe_allow_html=True)
                st.success("Transcription completed!")
            else:
                st.error("Transcription failed. Please check your audio file or conversion process.")

    # Diarization step
    if st.button("Run Diarization"):  # Enable diarization only if there's an uploaded file
        diarization_placeholder = st.empty()

        with st.spinner("Diarizing..."):
            speaker_segments = diarize_audio(uploaded_file)

            # Display diarization results
            if speaker_segments:
                diarization_placeholder.markdown('<h3>Speaker Diarization</h3>', unsafe_allow_html=True)
                for segment in speaker_segments:
                    diarization_placeholder.markdown(f'<div class="diarization-box">{segment}</div>', unsafe_allow_html=True)
                st.success("Diarization completed!")
            else:
                st.error("Diarization failed. Please check the audio file or diarization process.")

# JavaScript for clickable timestamps
st.markdown("""
    <script>
    function jumpToTime(time) {
        var audio = document.querySelector('audio');
        if (audio) {
            audio.currentTime = time;
            audio.play();
        }
    }
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('a[href^="#jump-"]').forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                var time = parseFloat(this.getAttribute('href').substring(6));
                jumpToTime(time);
            });
        });
    });
    </script>
""", unsafe_allow_html=True)
