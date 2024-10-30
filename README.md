<div align="center">
<h2>
    MinuteMate: Speeding up Municipal Communication
</h2>
<img width="300" alt="A fun logo" src="assets\Fun_Logo.jpg">
</div>

# 📄 Project Overview

MinuteMate improves how municipalities communicate with their citizens by simplifying the creation of meeting minutes. Upload your meeting audio and get formatted, ready-to-use minutes in less time. This ensures faster, clearer communication between local governments and their communities, providing key points, agenda items, and voting outcomes quickly and efficiently.

## Components of MinuteMate
* AV->Text Preprocessing Pipeline with Whisper: Includes transcription of audio to text as well as attribution of text to specific speakers.
* [Verba+Weaviate](https://github.com/dsba6010-llm-applications/MinuteMate/blob/main/Verba/README.md): Provides RAG preprocessing of text files (from document management and tokenization to vector embedding), vector database hosting with Weaviate, and a prompting interface. The Verba frontend and Weaviate vector database backend are deployed together, optionally via a single Dockerfile.  They must be supported by LLM integrations for vector embedding and for prompting (these need not be the same).
* [Llama on Modal](/llama_modal/Llama3_modal_serving.md): An option for serving an LLM.
* [Streamlit frontend for Llama](/streamlit_modal/streamlit_on_modal.md): A limited front-end for interacting with a Modal-hosted LLM 
* [Notebooks](/notebooks/prompting_with_modal.ipynb): A notebook for Python-based prompting for testing purposes

<img width="800" alt="A system diagram covering both the preprocessing pipeline and the prompt and response processes" src="assets\System_Diagram.svg">

# 🛠️ Documentation

[Whisper AV->Text Preprocessing Pipeline](Audio-Text/WHISPER_AV_TO_TEXT.md) - this includes a preprocessing pipeline to convert audiovisual information to text so that it can be cleaned and ingested into the RAG preprocessing pipeline in MinuateMate-Verba. 

[MinuteMate-Verba](Verba/VERBA.md) - this includes primary front-end of the app (based on Verba) and its integrations as well as a local deployment option of the vector database Weaviate.

[Contribution guidelines](docs/CONTRIBUTING.md) - Guidelines and instructions for contributing to the project
