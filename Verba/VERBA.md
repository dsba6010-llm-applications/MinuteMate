## Overview of Verba

### Key Components & Integration Options 

Input Data Source (Optional): 

Embedding Model: Weaviate, Ollama, SentenceTransformers, Cohere, VoyageAI, OpenAI

Chat Model: Ollama, Huggingface, Cohere, Anthropic, OpenAI, Groq

Vector Database: Weaviate (docker), Weaviate (SaaS)

### Preprocessing Pipelines

Import workflows: Unstructured, Firecrawl, GitHub/GitLab, AssemblyAI (Multi-Modal), .PDF, .CSV/.XLSX, .DOCX 

### NLP and Chunking Techniques

Chunking Techniques: spaCy Token, spaCy Sentence, Semantic, Recursive rule-based, HTML, Markdown, Code, JSON

### RAG Features

Vector DB Search: Keyword, Semantic, Hybrid

Autocomplete Suggestion

Filtering

Customizable Metadata

Async Ingestion

RAG pipeline in LangChain


## Deploying Verba

1. Install Docker

2. Clone the project

3. Set up API keys in a .env file.  You can base this on Verba/goldenverba/.env.example file. 

4. Docker stuff


```
docker compose --env-file <your-env-file> up -d --build
```

### API Keys

You can set all API keys in the Verba frontend, but to make your life easier, we can also prepare a `.env` file in which Verba will automatically look for the keys. Create a `.env` in the same directory you want to start Verba in. You can find an `.env.example` file in the [goldenverba](./goldenverba/.env.example) directory.

### Vector Database Options

Verba provides flexibility in connecting to Weaviate instances based on your needs. You have three options:

1. **Local Deployment**: Use Weaviate Embedded which runs locally on your device (except Windows, choose the Docker/Cloud Deployment)
2. **🐳 Docker Deployment**: Choose this option when you're running Verba's Dockerfile.
3. **🌩️ Cloud Deployment**: Use an existing Weaviate instance hosted on S WCD to run Verba. [Weaviate Cluster Setup Guide](https://weaviate.io/developers/wcs/guides/create-instance)

![Deployment in Verba](https://github.com/weaviate/Verba/blob/2.0.0/img/verba_deployment.png)

## Local Models w/ Ollama

Verba supports Ollama models. Download and Install Ollama on your device (https://ollama.com/download). Make sure to install your preferred LLM using `ollama run <model>`.

Tested with `llama3`, `llama3:70b` and `mistral`. The bigger models generally perform better, but need more computational power.

> Make sure Ollama Server runs in the background and that you don't ingest documents with different ollama models since their vector dimension can vary that will lead to errors

You can verify that by running the following command

```
ollama run llama3
```
