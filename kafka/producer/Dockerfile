# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /

# Copy local files into the container
COPY kafka/producer/requirements.txt ./
COPY kafka/producer/system_metrics_producer.py ./

# Install system dependencies needed for building psutil (and other Python packages with C extensions)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    build-essential \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the producer script
CMD ["python", "system_metrics_producer.py"]
