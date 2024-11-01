<div align="center">
<h2>
    MinuteMate: Speeding up Municipal Communication
</h2>
<img width="300" alt="A fun logo" src="assets\Fun_Logo.jpg">
</div>

# 📄 Overview

MinuteMate improves how municipalities communicate with their citizens by simplifying the creation of meeting minutes. Upload your meeting audio and get formatted, ready-to-use minutes in less time. This ensures faster, clearer communication between local governments and their communities, providing key points, agenda items, and voting outcomes quickly and efficiently.

## Diagram

<img width="800" alt="A system diagram covering both the preprocessing pipeline and the prompt and response processes" src="docs\system_diagram.svg">

##  Components

* [MinuteMate-Verba](Verba/README.md): the core of the app, based on Weaviate's [Verba](https://github.com/weaviate/Verba).  This includes the front end and back end (or integrations) for the RAG document management and pre-processing pipeline and the chat interface as well as a local deployment option of the vector database Weaviate.  At minimum, it relies on external integrations for the vector embedding model and for the prompting/chat model.  The Verba frontend and Weaviate vector database backend can be deployed together via a single Dockerfile.

* [Llama on Modal](/Llama_On_Modal/README.md): An option for serving a Llama model on Modal.

* [Notebooks](notebooks/): This will include notebooks for testing or interacting with various components of the app.

## 🛠️ Contributing

[Contribution guidelines](docs/CONTRIBUTING.md) - Guidelines and instructions for contributing to the project
