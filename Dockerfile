# Use an official Python runtime as a parent image
FROM python:3.11.2

# Set the working directory inside the container to /personalWebpage/personalWebpage
WORKDIR /personalWebpage/personalWebpage

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /personalWebpage/personalWebpage
COPY personalWebpage /personalWebpage/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /personalWebpage/requirements.txt

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED 1

# Run Gunicorn as the command
CMD ["gunicorn", "personalWebpage.wsgi:application", "--bind", "0.0.0.0:8000"]
