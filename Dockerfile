FROM python:3.11.2

WORKDIR /personalWebpage/django

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl gnupg \
    grep \
    && rm -rf /var/lib/apt/lists/*
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install -y nodejs

RUN npm install -g wscat

COPY django/requirements.txt /django/requirements.txt

RUN pip install --no-cache-dir -r /django/requirements.txt

EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED 1

