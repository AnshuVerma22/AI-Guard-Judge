FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements-api.txt .

# Install API dependencies
RUN pip install --no-cache-dir -r requirements-api.txt

# Copy application code
COPY app ./app

# Copy policy documents
COPY data ./data

EXPOSE 8000

# Build the vector database, then start the API
CMD ["sh", "-c", "python app/services/vector_store.py && uvicorn app.api:app --host 0.0.0.0 --port 8000"]