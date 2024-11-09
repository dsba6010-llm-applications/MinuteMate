FROM python:3.11-slim
WORKDIR /App
COPY . /App
RUN python -m pip install -r requirements.txt
EXPOSE 8000
CMD [" ", "start","--port","8001","--host","0.0.0.0"]