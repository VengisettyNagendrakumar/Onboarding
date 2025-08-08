FROM python:3.12-slim

# Install system dependencies for PyAudio and compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        portaudio19-dev \
        python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run your FastAPI/Uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]