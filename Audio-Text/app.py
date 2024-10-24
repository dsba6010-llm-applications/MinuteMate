import streamlit as st
from handler import transcribe_with_whisper, diarize_audio
import time

# Set page configuration and background
st.set_page_config(page_title="Minute Mate", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: white;
    }
    .title {
        font-size: 48px;
        font-weight: bold;
        text-align: center;
        color: #333333;
    }
    .subtitle {
        font-size: 24px;
        text-align: center;
        color: #666666;
        margin-bottom: 30px;
    }
    .transcription-box {
        width: 600px;
        height: 300px;
        overflow-y: scroll;
        border: 1px solid #dddddd;
        padding: 15px;
        background-color: #f7f7f7;
        font-family: monospace;
    }
    .diarization-box {
        width: 600px;
        height: 200px;
        overflow-y: scroll;
        border: 1px solid #dddddd;
        padding: 15px;
        background-color: #f0f0f0;
        font-family: monospace;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and Subtitle
st.markdown('<h1 class="title">Minute Mate</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="subtitle">ML-powered Minute Taking Tool</h2>', unsafe_allow_html=True)

# Upload audio file
uploaded_file = st.file_uploader("Drop your audio file here", type=["wav", "mp3", "m4a"])

# Audio Player
if uploaded_file is not None:
    st.audio(uploaded_file)

    # Transcription step
    if st.button("Transcribe Audio"):
        with st.spinner("Transcribing..."):
            transcription_placeholder = st.empty()  # Placeholder for live transcription
            transcription_data = transcribe_with_whisper(uploaded_file)

            if transcription_data:  # Check if transcription data is valid
                all_chunks = ""  # For storing the full transcription

                # Display live transcription chunks
                for chunk in transcription_data:
                    all_chunks += chunk + "\n"
                    transcription_placeholder.markdown(f'<div class="transcription-box">{all_chunks}</div>', unsafe_allow_html=True)
                    time.sleep(1)  # Simulate live transcription delay

                st.success("Transcription completed!")

            else:
                st.error("Transcription failed. Please check your audio file or conversion process.")

    # Diarization step
    if uploaded_file and st.button("Run Diarization"):  # Enable diarization only if there's an uploaded file
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
