FROM python:3.11.2

WORKDIR /personalWebpage/django

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY django /django/

RUN pip install --no-cache-dir -r /django/requirements.txt

# Expose the port that Gunicorn will run on
EXPOSE 8000

# Define environment variable
ENV PYTHONUNBUFFERED 1

# CMD ["gunicorn", "personalWebpage.wsgi:application", "--bind", "0.0.0.0:8000"]