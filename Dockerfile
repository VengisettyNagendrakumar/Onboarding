FROM python:3.12-slim

# Install system dependencies (for PyAudio if needed)
RUN apt-get update && \
    apt-get install -y portaudio19-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy server-specific requirements
COPY requirements-server.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Run the WebSocket server
CMD ["python", "serve1.py"]
