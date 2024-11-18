import assemblyai as aai
from utils.azure_blob_utils import download_from_azure  # For Azure integration
import os
from utils.env_setup import load_env

# Load environment variables
load_env()
ASSEMBLY_AI_KEY = os.getenv("ASSEMBLY_AI_KEY")
aai.settings.api_key = ASSEMBLY_AI_KEY
transcriber = aai.Transcriber()

def transcribe_audio(raw_file_name, model="best", speaker_labels=False):
    """
    Transcribes an audio file using AssemblyAI directly from Azure Blob Storage.

    Parameters:
    - raw_file_name (str): Name of the raw file in Azure Blob Storage to transcribe.
    - model (str): Transcription model to use ("best" or "nano").
    - speaker_labels (bool): Whether to enable speaker diarization.

    Returns:
    - str: Transcribed text, or None if transcription fails.
    """
    try:
        # Step 1: Download raw audio from Azure Blob Storage
        raw_content = download_from_azure("raw", raw_file_name, as_text=False)
        print(f"Downloaded {raw_file_name} from Azure for transcription.")

        # Step 2: Map transcription model
        if model == "nano":
            speech_model = aai.SpeechModel.nano
        else:
            speech_model = aai.SpeechModel.best

        # Step 3: Configure transcription
        config = aai.TranscriptionConfig(
            speech_model=speech_model,
            speaker_labels=speaker_labels
        )

        # Step 4: Start transcription
        print("Starting transcription...")
        transcript = transcriber.transcribe_audio_bytes(raw_content, config)
        
        # Step 5: Handle response
        if transcript.status == aai.TranscriptStatus.error:
            print(f"Transcription error: {transcript.error}")
            return None
        
        print("Transcription completed successfully.")
        return transcript.text

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
