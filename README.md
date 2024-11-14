# MinuteMate
<div align="center">
<img width="300" alt="A fun logo" src="assets\Fun_Logo.jpg">
</div>

### 📄 Overview

MinuteMate improves how municipalities communicate with their citizens by simplifying the creation of meeting minutes. Upload your meeting audio and get formatted, ready-to-use minutes in less time. This ensures faster, clearer communication between local governments and their communities, providing key points, agenda items, and voting outcomes quickly and efficiently.

### System Design Target

<img width="800" alt="A system diagram covering the preprocessing pipeline" src="docs\preprocessing_pipeline.svg">

<img width="800" alt="A system diagram covering the prompt and response processes" src="docs\prompt_and_response.svg">


### Major Components

- [**MinuteMate App**](MinuteMate/) - The public-facing chat application (in development).  This requires integration with the vector database, an embedding model (must match one of the embedding models used for preprocessing), and at least one generation model. Other possible integrations include a RAG-reranking model.  

- [**Preprocessing Pipeline**](Preprocessing/) - A set of tools to tranform raw audio and text files into vector-indexed chunks.  At minimum, it requires integration with an audio transcription model (currently AssemblyAI), an embedding model, and the vector database (currently Weaviate) which will serve as the repository. Other possible integrations include a generative model to be used to assist with data cleaning.

- [**Llama on Modal**](/Llama_On_Modal/) - Deploys [Llama](https://www.llama.com/) models to be served by [Modal](https://modal.com/).  This provides both generative and embedding models for use by other major components.

- [**Dev Notebooks**](dev_notebooks/) - This includes various notebooks for developing or testing components of the preprocessing pipeline and application.

### 🛠️ Contributing

[Contribution guidelines](docs/CONTRIBUTING.md) - Guidelines and instructions for contributing to the project
