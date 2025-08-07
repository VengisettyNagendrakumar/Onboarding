FROM python:3.12-slim

# Install system dependencies required by PyAudio
RUN apt-get update && \
    apt-get install -y portaudio19-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

# Copy all code
COPY . .

# Run your websocket server
CMD ["python", "server1.py"]
