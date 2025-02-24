from kafka import KafkaConsumer
import psycopg2
import json
import time

# Kafka Consumer
consumer = KafkaConsumer(
    'system_metrics',
    bootstrap_servers='kafka:9092',
    auto_offset_reset='latest',
    enable_auto_commit=True
)

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="personalWebpage_db",
    user="Krusovice",
    password="fedefrede",
    host="postgres_db",
    port="5432"
)
cursor = conn.cursor()

while True:
    messages = consumer.poll(timeout_ms=5000)  # Poll Kafka every 5 sec
    if messages:
        for _, records in messages.items():
            for record in records:
                data = json.loads(record.value.decode('utf-8'))
                cursor.execute(
                    "INSERT INTO system_metrics_table (timestamp, cpu_usage, ram_usage) VALUES (%s, %s, %s)",
                    (data['timestamp'], data['cpu_usage'], data['ram_usage'])
                )
    conn.commit()
    time.sleep(5)  # Wait 5 seconds before next poll
