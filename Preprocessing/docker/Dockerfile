# Dockerfile to set up the environment for Streamlit app

# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY docker/requirements.txt .
RUN pip install -r requirements.txt

# Copy the application files
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Run the Streamlit application
CMD ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
