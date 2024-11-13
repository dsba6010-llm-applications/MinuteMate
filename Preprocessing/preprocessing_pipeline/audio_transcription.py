import assemblyai as aai
import os
from utils.env_setup import load_env

# Load environment variables
load_env()
ASSEMBLY_AI_KEY = os.getenv("ASSEMBLY_AI_KEY")
aai.settings.api_key = ASSEMBLY_AI_KEY
transcriber = aai.Transcriber()

def transcribe_audio(file, model="best", speaker_labels=False):
    """
    Transcribes an audio file using AssemblyAI with specified model and speaker labels option.

    Parameters:
    - file: file-like object, the uploaded audio file to transcribe
    - model: str, transcription model to use ("best" or "nano")
    - speaker_labels: bool, whether to enable speaker diarization

    Returns:
    - str: Transcribed text
    """
    # Map the model selection to AssemblyAI's model classes
    if model == "nano":
        speech_model = aai.SpeechModel.nano
    else:
        speech_model = aai.SpeechModel.best

    # Save the file temporarily for the SDK to access
    temp_file_path = "temp_audio_file.wav"  # You can choose a unique name or path
    with open(temp_file_path, "wb") as f:
        f.write(file.read())

    # Create the transcription configuration with model and speaker labels
    config = aai.TranscriptionConfig(
        speech_model=speech_model,
        speaker_labels=speaker_labels
    )

    # Transcribe the audio
    try:
        transcript = transcriber.transcribe(temp_file_path, config)
    except aai.TranscriptionError as e:
        print(f"Transcription failed: {e}")
        return None

    if transcript.status == aai.TranscriptStatus.error:
        print(f"Transcription error: {transcript.error}")
        return None

    # Clean up the temporary file
    os.remove(temp_file_path)

    # Return the transcribed text
    return transcript.text
