##### Preprocessing Pipeline

<img width="800" alt="A system diagram covering the preprocessing pipeline" src="..\docs\preprocessing_pipeline.svg">

##### Preprocessing Stages

- **Curation** - First, a human must decide what documents to include in the corpus and how to organize them.
- **Transcription** - Audio recordings of the meetings are sent to a transcription service.  The resulting text includes speaker attribution.
- **PDF Conversion** - PDFs of agendas, minutes, or other text documents are converted to raw text for further processing.
- **Enrichment** - Metadata is added by humans, for example to identify meeting dates, document types, meeting types, key participants in meetings.
- **Cleaning** - Using available text and metadata, a partially-automated cleaning process is applied, where automated systems attempt to identify and flag or correct suspected errors in transcription for human review.
- **Chunking, Tokenization, Embedding** - Cleaned documents are broken up into chunks, using different methods depending on document type (as indicated by document metadata). The size and composition of these chunks must be designed to support the extraction of effective keywords and the generation of effective embeddings. The chunks are then sent to an embedding service where they are tokenized and vectorized.  The resulting vector embeddings are used to index the chunks to support vector and hybrid search.
- **Database Ingestion** - The documents are indexed in a vector database according to their vector embeddings and key words.  A different collection is created for each model used for vector embeddings.

##### Setup Instructions

TODO