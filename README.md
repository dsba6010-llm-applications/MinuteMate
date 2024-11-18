# MinuteMate
<div align="center">
<img width="600" alt="A fun logo" src="assets\Fun_Logo.jpg">
</div>

### 🌞 Enabling Transparency

MinuteMate improves how municipalities communicate with their citizens by simplifying the creation of meeting minutes. Upload your meeting audio and documents and present a queriable interface to the public to get the most out of government transparency.

### 🧭 System Diagram

<img width="800" alt="A system diagram covering the preprocessing pipeline" src="docs\preprocessing_pipeline.svg">

<img width="800" alt="A system diagram covering the prompt and response processes" src="docs\prompt_and_response.svg">

### ⚙️ Major Components

- [**MinuteMate App**](MinuteMate/) - The public-facing chat application (in development).  This requires integration with the vector database, an embedding model (must match one of the embedding models used for preprocessing), and at least one generation model. Other possible integrations include a RAG-reranking model.

- [**Preprocessing Pipeline**](Preprocessing/) - A set of tools to tranform raw audio and text files into vector-indexed chunks.  At minimum, it requires integration with an audio transcription model (currently AssemblyAI), an embedding model, and the vector database (currently Weaviate) which will serve as the repository. Other possible integrations include a generative model to be used to assist with data cleaning.

- [**Llama on Modal**](/Llama_On_Modal/) - Deploys [Llama](https://www.llama.com/) models to be served by [Modal](https://modal.com/).  This provides both embedding and generative models for use by other major components.

- [**Dev Notebooks**](dev_notebooks/) - This includes various notebooks for developing or testing components of the preprocessing pipeline and application.

### 🏭 Setup and Deployment

- Clone this repository
- Curate a corpus of information you want to present
- Deploy embedding or generative models (optional)
- Set up a RAG database (usually a vector database)
- Preprocess your corpus to populate the RAG database 
- Deploy the backend to handle prompt and response logic 
- Deploy the frontend 

### 💡 Meet the Team

- Aboli Kasar - [LinkedIn](https://www.linkedin.com/in/abolikasar)|
- Yash Pradhan - [LinkedIn](https://www.linkedin.com/in/iamyashpradhan/)|
- Riley LePrell - [LinkedIn](https://www.linkedin.com/in/riley-leprell)|
- Neal Logan - [LinkedIn](https://www.linkedin.com/in/nealdlogan))

### 🛠️ How To Contribute

[Contribution guidelines](docs/CONTRIBUTING.md) - Guidelines and instructions for contributing to the project
