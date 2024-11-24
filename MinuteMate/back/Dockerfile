FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8001
CMD ["uvicorn", "main:app","--host","0.0.0.0","--port","8001"]