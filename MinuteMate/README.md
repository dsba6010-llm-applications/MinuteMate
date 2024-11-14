##### Prompt and Response

<img width="800" alt="A system diagram covering the preprocessing pipeline" src="..\docs\prompt_and_response.svg">

##### Front-end Components & Integration

- **Chat Interface** - TODO

##### Back-end Components & Integrations

- **API Layer** - Exposes an API that the front end consumes
- **Query Preparation** - Extract keywords, get vector embeddings of prompt or parts of prompt, if necessary.  The embedding model(s) used at this stage MUST match the embedding models of the database collections to be queried.
- **Database Query** - Uses extracted keywords, vector embeddings, and/or other relevant information to get relevant chunks from the vector database, as provided by the preprocessing pipeline.
- **Reranking & Filtering** - Selects resources for response, potentially using an external reranking service.
- **Response Generation** - Generates a response, typically by sending a request to a generative model with the original user prompt and a system prompt including selected resources acquired from the vector database. 
- **Trust & Safety** - Two separate stages, each using an external generative model.  The first stage examines only the incoming prompt.  If an inappropriate prompt is detected at this stage, all ordinary steps are skipped and a response is sent declining the prompt.  The second examines generated responses and vetoes those with inappropriate content.

##### Setup - Docker

TODO

