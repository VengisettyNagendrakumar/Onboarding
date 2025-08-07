# FROM python:3.12-slim

# # Install system dependencies
# RUN apt-get update && \
#     apt-get install -y portaudio19-dev gcc && \
#     rm -rf /var/lib/apt/lists/*

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy the rest of the code
# COPY . .

# # Start your app
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
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

# Run your websocket server
CMD ["python", "server.py"]
