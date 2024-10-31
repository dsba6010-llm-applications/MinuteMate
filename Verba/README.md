## Overview of Verba

Verba provides a framework for a RAG application.  The implementation in this project will be limited and modified.  For detailed information about Verba, see the [Verba](https://github.com/weaviate/Verba/blob/main/README.md) repository. 

### Key Components & Integration Options 

**Ingestion Capabilities and Integrations**: 
- Capabilities: .PDF, .CSV/.XLSX, .DOCX, and GitHub/GitLab  
- Integrations: [Unstructured](https://unstructured.io/) data, [Firecrawl](https://www.firecrawl.dev/) web crawler, [AssemblyAI](https://assemblyai.com/) multi-modal import

**Chunking Techniques**: 
- spaCy Token & Sentence, 
- Semantic, 
- Recursive rule-based, 
- Code: HTML, Markdown, Code, JSON

**Embedding Model Integrations**: Weaviate, Ollama, SentenceTransformers, Cohere, VoyageAI, OpenAI

**Vector Database Integrations**: Weaviate (docker), Weaviate (SaaS)

**Chat Model Integrations**: Ollama, Huggingface, Cohere, Anthropic, OpenAI, Groq

### RAG Features

Vector DB Search: Keyword, Semantic, Hybrid
Autocomplete Suggestion
Filtering
Customizable Metadata
Async Ingestion
RAG pipeline in LangChain

## Deploying Verba Locally with Docker
See Verba docs for other deployment options

1. Preparation:
- Install Docker Desktop
- Make sure Docker Desktop is running
- Clone the project repository

2. Set up required external components and place API keys in a .env file in Verba/goldenverba.  You can base this on [Verba/goldenverba/.env.example](/Verba/goldenverba/.env.example).  

3. You can use the `docker-compose.yml` to add required environment variables under the `verba` service and can also adjust the Weaviate Docker settings to enable Authentification or change other settings of your database instance. You can read more about the Weaviate configuration in our [docker-compose documentation](https://weaviate.io/developers/weaviate/installation/docker-compose)

> Please make sure to only add environment variables that you really need.

4. From the Verba folder, run the following commands to download the necessary Docker images, create containers, and start Verba:

```bash
docker compose up -d
```

```bash
docker compose --env-file goldenverba/.env up -d --build
```

5. Access Verba and Weaviate via web browser:

- You can access the Verba frontend at `localhost:8000`

- You can also access your local Weaviate instance at `localhost:8080`

6.  Select deployment type

- **🐳 Docker Deployment** - using a separate Weaviate instance that is running inside the same Docker network, which is deployed when using Verba's default Dockerfile.
- **🌩️ Weaviate Cloud Deployment** - using a Weaviate instance that is hosted on Weaviate Cloud Services (WCS).  [Weaviate Cluster Setup Guide](https://weaviate.io/developers/wcs/guides/create-instance)
- **Custom Deployment** - allows you to specify your own Weaviate instance URL, PORT, and API key.

## Deploying Local Models w/ Ollama

Verba supports Ollama models. Download and Install Ollama on your device (https://ollama.com/download). Make sure to install/run your preferred LLM using `ollama run <model>`.

Tested with `llama3`, `llama3:70b` and `mistral`. The bigger models generally perform better, but need more computational power.

> Make sure Ollama Server runs in the background and that you don't ingest documents with different ollama models since their vector dimension can vary that will lead to errors

You can verify that by running the following command

```
ollama run llama3
```
