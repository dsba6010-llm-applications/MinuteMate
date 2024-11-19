import os
import requests
from utils.azure_blob_utils import download_from_azure
from utils.env_setup import load_env

# Load environment variables
load_env()
ASSEMBLY_AI_KEY = os.getenv("ASSEMBLY_AI_KEY")
ASSEMBLY_AI_ENDPOINT = "https://api.assemblyai.com/v2"

def transcribe_audio(raw_file_name, model=None, speaker_labels=False):
    """
    Transcribes an audio file using AssemblyAI.

    Parameters:
    - raw_file_name (str): Name of the raw file in Azure Blob Storage.
    - model (str): Transcription model to use (not currently implemented in AssemblyAI).
    - speaker_labels (bool): Whether to enable speaker diarization.

    Returns:
    - str: Transcribed text, or None if transcription fails.
    """
    headers = {"authorization": ASSEMBLY_AI_KEY}
    try:
        # Step 1: Download the raw audio file from Azure
        raw_content = download_from_azure("raw", raw_file_name, as_text=False)
        print(f"Downloaded {raw_file_name} from Azure for transcription.")

        # Step 2: Upload the audio file to AssemblyAI
        print("Uploading audio file to AssemblyAI...")
        upload_response = requests.post(
            f"{ASSEMBLY_AI_ENDPOINT}/upload",
            headers=headers,
            data=raw_content
        )
        if upload_response.status_code != 200:
            print(f"Error uploading to AssemblyAI: {upload_response.status_code} - {upload_response.text}")
            return None

        upload_url = upload_response.json()["upload_url"]
        print(f"File uploaded to AssemblyAI. URL: {upload_url}")

        # Step 3: Request transcription
        print("Requesting transcription from AssemblyAI...")
        transcription_payload = {"audio_url": upload_url}
        
        if speaker_labels:
            transcription_payload["speaker_labels"] = True
        
        transcription_response = requests.post(
            f"{ASSEMBLY_AI_ENDPOINT}/transcript",
            headers=headers,
            json=transcription_payload
        )
        if transcription_response.status_code != 200:
            print(f"Error submitting transcription request: {transcription_response.status_code} - {transcription_response.text}")
            return None

        transcription_id = transcription_response.json()["id"]
        print(f"Transcription request submitted. ID: {transcription_id}")

        # Step 4: Poll for transcription result
        while True:
            status_response = requests.get(
                f"{ASSEMBLY_AI_ENDPOINT}/transcript/{transcription_id}",
                headers=headers
            )
            status_response.raise_for_status()
            data = status_response.json()

            if data["status"] == "completed":
                print("Transcription completed successfully.")
                return data["text"]
            elif data["status"] == "failed":
                print(f"Transcription failed: {data['error']}")
                return None
            else:
                print("Transcription in progress... Retrying in 5 seconds.")
                import time
                time.sleep(5)

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
