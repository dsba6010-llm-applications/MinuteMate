FROM python:3.11
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run","app.py"]
