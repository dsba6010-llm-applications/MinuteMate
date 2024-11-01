# Overview of MinuteMate-Verba

Verba provided a framework for a RAG application, and we have modified this to create MinuteMate.  For detailed information about Verba, see the [Verba](https://github.com/weaviate/Verba/) repo. 

# Deploying MinuteMate-Verba

## Local Docker Deployment
*See Verba docs for other deployment options*

1. Preparation:
- Install Docker Desktop
- Make sure Docker Desktop is running
- Clone the project repository

2. Set up required external components and obtain any necessary URLs and API keys.  See the **External Dependencies** section below for more details.
- Ingestion: If you're importing files in .PDF, .CSV/.XLSX, .DOCX, or other text-based formats, there are no external dependencies.  If you're preprocessing audio data, you will need a transcription service, and AssemblyAI is currently the only integration available.  For other ingestion options such as web crawling and unstructured data, see the Verba documentation.
- Vector database: always required.  Weaviate is currently the only option, but can be deployed in a few ways.  This document covers only the Weaviate Cloud option.
- Embedding model service: always required. This must be the same as the embedding model used to populate the vector database.
- Generative model service: always required. This can be whichever chat model or service you prefer.

3. Place all required URLs and API keys in a .env file in the Verba folder.  You can base this on '.env.example'; simply rename the file to .env and add relevant variables.  These variables are passed along to the Docker container environment as specified in `docker-compose.yml`.  So if you need to add variables to that environment, you must add them in both your .env file and in 'docker-compose.yml'.  

> Please make sure to only add environment variables that you really need.

4. From the Verba folder, run the following command to create a Docker images, create a container, and start Verba within that container:

```bash
docker compose --env-file goldenverba/.env up -d --build
```

5. Access Verba interface via web browser:
- You can access the Verba frontend at `localhost:8000`

6.  Select deployment type
- Select **🌩️ Weaviate Cloud Deployment** - using a Weaviate instance that is hosted on Weaviate Cloud Services (WCS).  [Weaviate Cluster Setup Guide](https://weaviate.io/developers/wcs/guides/create-instance)
- For other deployment options, see the Verba documentation.

# External Dependencies 

## Preprocessing Audio Data

### AssemblyAI

[AssemblyAI](https://assemblyai.com/) provides transcription services.

## Vector Database

### Weaviate

You can read more about the Weaviate configuration in our [docker-compose documentation](https://weaviate.io/developers/weaviate/installation/docker-compose)

## Embedding and Generative Models

**Embedding Model Integrations**: Weaviate, Ollama, SentenceTransformers, Cohere, VoyageAI, OpenAI

**Chat Model Integrations**: Ollama, Huggingface, Cohere, Anthropic, OpenAI, Groq

### Deploying Llama on Modal 

See the [Llama_On_Modal](/Llama_On_Modal/README.md) component of this project.

### Deploying Local Models w/ Ollama

Verba supports Ollama models. Download and Install Ollama on your device (https://ollama.com/download). Make sure to install/run your preferred LLM using `ollama run <model>`.

Tested with `llama3`, `llama3:70b` and `mistral`. The bigger models generally perform better, but need more computational power.

> Make sure Ollama Server runs in the background and that you don't ingest documents with different ollama models since their vector dimension can vary that will lead to errors

You can verify that by running the following command

```
ollama run llama3
```