import torch
import torchaudio
import tempfile
import os
import streamlit as st
from transformers import WhisperProcessor, WhisperForConditionalGeneration
from pyannote.audio import Pipeline  # Import Diarization Pipeline
import time

# Load Whisper model and processor directly from Hugging Face
model_name = "openai/whisper-small"
processor = WhisperProcessor.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

def save_uploaded_audio(uploaded_file):
    """Save the uploaded audio file to a temporary file for processing."""
    try:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            temp_wav.write(uploaded_file.getbuffer())  # Save the uploaded file to a temporary location
            return temp_wav.name
    except Exception as e:
        st.error(f"Error saving audio file: {e}")
        return None

def transcribe_with_whisper(audio_file):
    # Convert audio to WAV format before loading
    converted_audio_path = save_uploaded_audio(audio_file)
    if not converted_audio_path:
        return None

    # Load the audio file with torchaudio
    waveform, sample_rate = torchaudio.load(converted_audio_path)

    # Resample the audio to 16 kHz (16000 Hz) if it's not already
    if sample_rate != 16000:
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        sample_rate = 16000

    # Convert to mono (if stereo)
    if waveform.size(0) > 1:
        waveform = torch.mean(waveform, dim=0, keepdim=True)

    # Initialize progress bar
    progress_bar = st.progress(0)

    # Initialize the transcription box to display live updates
    transcription_placeholder = st.empty()

    # Split waveform into 15-second chunks
    chunk_size = sample_rate * 15  # 15 seconds worth of audio
    chunks = [waveform[:, i:i+chunk_size] for i in range(0, waveform.size(1), chunk_size)]

    all_transcriptions = []
    total_duration = waveform.size(1) / sample_rate  # Total duration of the audio in seconds

    for i, chunk in enumerate(chunks):
        # Calculate the start time of the current chunk
        chunk_start_time = (i * chunk_size) / sample_rate

        # Format the timestamp (e.g., "00:00:00")
        timestamp = f"{int(chunk_start_time // 3600):02}:{int((chunk_start_time % 3600) // 60):02}:{int(chunk_start_time % 60):02}"

        # Process the 15-second chunk with Whisper
        inputs = processor(chunk.squeeze(0), sampling_rate=sample_rate, return_tensors="pt")
        predicted_ids = model.generate(inputs.input_features)
        transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        # Simulate word-by-word updates for each chunk
        words = transcription.split(" ")
        current_transcription = ""
        for word in words:
            current_transcription += f"{word} "
            transcription_placeholder.markdown(f"**Live Transcription**\n\n{current_transcription.strip()}", unsafe_allow_html=True)
            time.sleep(0.1)  # Simulate delay for word-by-word update

        # Append the full 15-second chunk's transcription with the timestamp
        formatted_transcription = f"[{timestamp}](#jump-{chunk_start_time}) - {transcription}"
        all_transcriptions.append(formatted_transcription)

        # Update the live transcription in the placeholder
        transcription_placeholder.markdown(f"**Live Transcription**\n\n" + "\n\n".join(all_transcriptions), unsafe_allow_html=True)

        # Update progress bar
        progress_bar.progress((i + 1) / len(chunks))

    full_transcription = "\n".join(all_transcriptions)

    # Clean up temporary files
    os.remove(converted_audio_path)

    return all_transcriptions

def diarize_audio(audio_file):
    # Load Pyannote diarization model
    hf_token = os.getenv("HF_TOKEN")  # Hugging Face token stored in environment
    diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=hf_token)

    # Save uploaded file temporarily
    saved_audio_path = save_uploaded_audio(audio_file)
    if not saved_audio_path:
        return None

    # Diarize the audio
    diarization_result = diarization_pipeline(saved_audio_path)

    # Create speaker-tagged transcript with overlapping speakers handled
    speaker_segments = []
    for segment, _, speaker in diarization_result.itertracks(yield_label=True):
        speaker_segments.append(f"Speaker {speaker}: {segment.start:.2f}s to {segment.end:.2f}s")

    # Clean up temporary audio file
    os.remove(saved_audio_path)

    return speaker_segments
