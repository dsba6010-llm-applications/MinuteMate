##### Setup

TODO

##### Preprocessing Stages

- **Curation** - First, a human must decide what documents to include in the RAG corpus and how to organize them. 
- **Transcription** - Audio recordings of the meetings are transcribed by AssemblyAI with speaker attribution. 
- **Enrichment** - Metadata is added to the documents by humans, for example to identify key participants in meetings and to link documents pertaining to the same meeting.
- **Cleaning** - Using available text and metadata, a partially-automated cleaning process is applied, where automated systems attempt to identify and flag or correct suspected errors in transcription for human review.
- **Chunking** - Documents are broken up into chunks.  The size and composition of these chunks should be designed to support the extraction of effective keywords and the generation of effective embeddings.
- **Keyword Extraction** - NLP tools are used to extract chunk-level keywords to support keyword and hybrid search.
- **Tokenization and Embedding** - The documents are broken up into tokens and vector embeddings are generated to support vector and hybrid search.
- **Database Ingestion** - The documents are indexed in a vector database according to their vector embeddings and key words.  A different collection is created for each model used for vector embeddings.