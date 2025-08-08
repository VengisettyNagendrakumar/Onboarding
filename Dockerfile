FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        portaudio19-dev \
        gcc \
        libffi-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port (Render still uses $PORT internally)
EXPOSE 5000

# Start the app with uvicorn (Render sets $PORT)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]