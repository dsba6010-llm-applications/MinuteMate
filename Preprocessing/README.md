# 🚀 Preprocessing Pipeline for Meeting Transcriptions and Documents

<img width="800" alt="A system diagram covering the preprocessing pipeline" src="../docs/preprocessing_pipeline.svg">

---

## 🌟 Overview

The **Preprocessing Pipeline** is a staff-facing application designed to streamline the transcription, cleanup, and vectorization of meeting-related documents such as agendas, minutes, and audio files. This tool enables municipal staff to:
- Upload 🖼️, process ⚙️, and view 👀 transformed documents at each stage.
- Ensure accurate and efficient management of meeting data 🏛️.
- Integrate metadata 📋 for organizational clarity.
- Use cutting-edge AI tools 🤖 to enhance transcription quality and create vector embeddings for further analysis.

---

## ✨ Features

### 🏠 Home Page
- Two main options:
  - **Upload Documents** 📤
  - **View Documents** 📂

### 📤 Upload Documents
- Staff can input metadata:
  - **📅 Meeting Date**: Any date.
  - **🏛️ Meeting Type**: Board of Commissioners or Planning Board.
  - **📄 File Type**: Agenda, Minutes, or Audio.
- Metadata is saved, and the file upload process begins.

#### For Audio Files 🎙️:
- Users can select an AssemblyAI model:
  - **Nano**: ⚡ Faster and cheaper but lower quality.
  - **Best**: 🏆 Higher quality but more expensive and slower.
- Files up to **1GB** can be uploaded.

#### Audio Processing Workflow:
1. 📥 **Upload**: Files are saved to Azure's "Raw Data" folder.
2. 🎧 **Transcription**: AssemblyAI transcribes the audio.
3. 🛠️ **Cleaning**: Transcriptions are saved in a "Dirty Folder," tokenized, chunked, and sent to OpenAI for cleaning (e.g., GPT-4.0, GPT-3.5).
4. 📜 **Clean Text**: A refined text file is saved back to Azure.
5. 📊 **Vectorization**: The cleaned text is embedded using **text-embedding-ada-002** and stored in Weaviate Cloud.

#### For Agendas and Minutes 📄:
1. 📥 **Upload**: Files are uploaded to Azure’s "Raw Data" folder.
2. 📄 **PDF-to-Text Conversion**: Files are converted to text using a PDF conversion utility.
3. 🛠️ **Cleaning**: The raw text is saved in a "Dirty Folder," tokenized, chunked, and sent to OpenAI for cleaning.
4. 📊 **Vectorization**: The cleaned text is embedded using **text-embedding-ada-002**.
5. 💾 **Storage**: Vectorized data is stored in Weaviate Cloud for further analysis and retrieval.

### 📂 View Documents
- Staff can download documents at any stage:
  - **Raw Audio** 🎵
  - **Dirty Transcriptions** 📝
  - **Clean Text** ✅

---

## ⚙️ Setting Up Locally

### 🔑 Prerequisites

1. **Create a `.env` file** with the following structure:

    ```env
    # OpenAI Setup
    OPENAI_API_KEY=
    OPENAI_BASE_URL=

    # Weaviate Cloud Deployment
    WEAVIATE_URL=
    WEAVIATE_API_KEY=

    # AssemblyAI Setup
    ASSEMBLY_AI_KEY=

    # Azure Storage Container Connection
    AZURE_STORAGE_CONNECTION_STRING=
    AZURE_STORAGE_CONTAINER_NAME=

    # Pathing Setup
    PYTHONPATH=
    ```

2. **API Keys Setup**:
    - **OpenAI**:
      - 🔗 [Get your API key](https://platform.openai.com/api-keys).
      - Set `OPENAI_API_KEY` in the `.env` file.
      - For `OPENAI_BASE_URL`, use `https://api.openai.com/v1` or leave it blank.
    - **Weaviate**:
      - 🔗 [Access your Weaviate cluster details](https://console.weaviate.cloud/cluster-details).
      - Follow [this guide](https://weaviate.io/developers/wcs/create-instance) to create a new cluster if needed.
      - Set `WEAVIATE_URL` with the REST endpoint and `WEAVIATE_API_KEY` with the admin key.
    - **AssemblyAI**:
      - 🔗 [Create an AssemblyAI account](https://www.assemblyai.com/app).
      - Copy your API key from the homepage and set it in `ASSEMBLY_AI_KEY`.
    - **Azure**:
      - 🔗 [Create a storage account](https://learn.microsoft.com/en-us/azure/storage/common/storage-account-create?tabs=azure-portal).
      - Go to the **Access Keys** section in Azure and copy the connection string into `AZURE_STORAGE_CONNECTION_STRING`.
      - Specify the container name in `AZURE_STORAGE_CONTAINER_NAME`.

3. **Python Path**:
    - Navigate to the `Preprocessing` folder in your project.
    - Copy its path and set it in the `PYTHONPATH` field of the `.env` file.
    - Example: 
       - PYTHONPATH=C:\Users\rleprell\Downloads\programming_directory\MinuteMate\Preprocessing


---

## 💻 Installation and Running Locally

1. **Install Requirements**:
    Run the following command to install dependencies:
    ```bash
    pip install -r docker/requirements.txt
    ```

2. **Run the Application**:
    Start the Streamlit application:
    ```bash
    streamlit run app/main.py
    ```
