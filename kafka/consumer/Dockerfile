# Use a lightweight Python image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /

# Copy local files into the container
COPY requirements.txt ./
COPY system_metrics_consumer.py ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the consumer script
CMD ["python", "app/system_metrics_consumer.py"]
