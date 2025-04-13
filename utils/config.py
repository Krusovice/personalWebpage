from utils import secrets

POSTGRES_CONFIG = {
    "dbname": "personalWebpage_db",
    "user": secrets.POSTGRES_USER,
    "password": secrets.POSTGRES_PASSWORD,
    "host": "postgres_db",
    "port": "5432"
}

DJANGO_SECRET_KEY = secrets.DJANGO_SECRET_KEY

KAFKA_CONFIG = {
    "bootstrap_servers": "kafka:9092",
    "auto_offset_reset": "latest",
    "enable_auto_commit": True
}

REDIS_CONFIG = {
    "host": "redis",
    "port": 6379
}