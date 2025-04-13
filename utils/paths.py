from pathlib import Path

# Root
ROOT_DIR = Path(__file__).resolve().parents[1]

# Directories
DATA_DIR = ROOT_DIR / "postgres_data"
KAFKA_DIR = ROOT_DIR / "kafka"
AIRFLOW_DIR = ROOT_DIR / "airflow"
DJANGO_DIR = ROOT_DIR / "django"