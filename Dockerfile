FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y portaudio19-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY . .

# Run your websocket server (✅ changed to serve1.py)
CMD ["python", "serve1.py"]
