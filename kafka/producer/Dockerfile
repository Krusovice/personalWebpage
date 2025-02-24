# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy local files into the container
COPY requirements.txt ./
COPY system_metrics_producer.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the producer script
CMD ["python", "system_metrics_producer.py"]
