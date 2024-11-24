##### Prompt and Response

<img width="800" alt="A system diagram covering the preprocessing pipeline" src="..\docs\prompt_and_response.svg">

##### Front-end Components & Integration

- **Chat Interface** - TODO

##### Back-end Components & Integrations

- **API Layer** - Exposes an API that the Streamlit front end consumes.  Uses FastAPI.
- **Query Preparation** - Extract keywords, and get vector embeddings of prompt or parts of prompt, as necessary.  The embedding model used to get vector embeddings at this stage MUST match the embedding models of the database collections to be queried or search results will be nonsense.
- **Database Query** - Uses extracted keywords, vector embeddings, and/or other relevant information to get relevant chunks from the vector database, as provided by the preprocessing pipeline.
- **Reranking & Filtering** - Selects resources for response, potentially using an external reranking service.
- **Response Generation** - Generates a response, typically by sending a request to a generative model with the original user prompt and a system prompt including selected resources acquired from the vector database. 
- **Trust & Safety** - Two separate stages, each using an external generative model.  The first stage examines only the incoming prompt.  If an inappropriate prompt is detected at this stage, all ordinary steps are skipped and a response is sent declining the prompt.  The second examines generated responses and vetoes those with inappropriate content.

##### Local Setup - Docker

- Start [**Docker Desktop**](https://www.docker.com/products/docker-desktop/)

- In folder **MinuteMate/back**, create file '.env' according to .env.example with necessary secrets

- Deploy FastAPI back end: In the folder **MinuteMate/back**, run:
```bash
docker compose --env-file .env up -d --build
```

- Deploy Streamlit front end: In the folder **MinuteMate/front**, run:
```bash
docker compose up -d --build
```

- To interact with the Streamlit Open a web browser and navigate to localhost:8501

- To close the Streamlit app, ensure Streamlit is still open in the browser, then at the command line used to deploy Streamlit, press and hold ctrl-C for at least 3 second  

- Shut down and clean up by deleting your Docker Containers and Docker Images in Docker Desktop

##### Setup - Repo

**Front-End
```
cd /MinuteMate/front/
streamlit run app.py
```

**Back-End
```
cd /MinuteMate/back/
uvicorn main:app --reload
```


