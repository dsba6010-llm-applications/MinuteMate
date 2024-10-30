

## AV->Text Preprocessing Pipeline with Whisper

### 📝 Transcribe Audio

```bash
pip install -U whisperplus
import nest_asyncio 
nest_asyncio.apply
```
```bash
pip install whisperplus git+https://github.com/huggingface/transformers
pip install flash-attn --no-build-isolation
pip install -r https://raw.githubusercontent.com/kadirnar/whisper-plus/main/requirements/speaker_diarization.txt
```

```python
from whisperplus import SpeechToTextPipeline, download_youtube_to_mp3
from transformers import BitsAndBytesConfig, HqqConfig
import torch

# This is used for setting audio path from a Youtube Video
# url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
# audio_path = download_youtube_to_mp3(url, output_dir="downloads", filename="test")

# This is setting audio_path with a file
audio_path = "Insert File"

hqq_config = HqqConfig(
    nbits=4,
    group_size=64,
    quant_zero=False,
    quant_scale=False,
    axis=0,
    offload_meta=False,
)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,
)

pipeline = SpeechToTextPipeline(
    model_id="distil-whisper/distil-large-v3", # Other model choices: openai/whisper-tiny, openai/whisper-small, openai/whisper-medium, openai/whisper-large-v2
    quant_config=hqq_config,
    flash_attention_2=True,
)

transcript = pipeline(
    audio_path=audio_path,
    chunk_length_s=30, # Length of Audio Chunks (seconds)
    stride_length_s=5, # Overlapping Length in Audio Chunks (seconds)
    max_new_tokens=128, # Max Tokens Genrated in a Chunk.
    batch_size=100, # Audio Chunks Processed at a Time. Lower = Faster
    language="english", # Chose a Language
    return_timestamps=True, # Enable Timestamps
)

print(transcript)
```

---

### 💬 Speaker Diarization

Speaker diarization helps assign portions of the transcript to specific speakers, helping you know who said what during the meeting.

You must confirm the licensing permissions of these two models:

- https://huggingface.co/pyannote/speaker-diarization-3.1
- https://huggingface.co/pyannote/segmentation-3.0

To set up a Hugging Face token, go to Settings -> Access Tokens, click Create New Token, set Token Type to Read, and then click Create.

To set up Hugging Face authentication, follow these steps:

#### Install and authenticate Hugging Face:

```bash
pip install -U "huggingface_hub[cli]"
from huggingface_hub import notebook_login
notebook_login()
```

#### Run the Speaker Diarization:

```python
from whisperplus.pipelines.whisper_diarize import ASRDiarizationPipeline
audio_path = "audio_only.m4a"
device = "cuda"  # cpu or "mps" for Apple Silicon devices

pipeline = ASRDiarizationPipeline.from_pretrained(
    asr_model="openai/whisper-large-v3",
    diarizer_model="pyannote/speaker-diarization-3.1",
    use_auth_token=True,
    chunk_length_s=10,
    device=device,
)

output_text = pipeline(audio_path)
print(output_text)
```

### 🤗 Shoutout

Audio transcription in this project is made possible thanks to the **WhisperPlus** basemodel, which is based on OpenAI's Whisper. Special thanks to Alec Radford, Jong Wook Kim, Tao Xu, Greg Brockman, Christine McLeavey, and Ilya Sutskever for their work on Whisper-Plus.

You can find their paper [here](https://arxiv.org/abs/2212.04356).
