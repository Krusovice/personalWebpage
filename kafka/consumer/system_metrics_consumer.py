print('consumer start')
import asyncio
from kafka import KafkaConsumer
import json
import time
#time.sleep(1000)
import psycopg2

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_app.personalWebpage.settings_consumer')
import django
django.setup()
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()

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

                # Send data to channel layer
                asyncio.run(channel_layer.group_send(
                    "metrics_group",
                    {"type": "metrics.message", "message": 'data'},
                ))
    conn.commit()
    time.sleep(5)  # Wait 5 seconds before next poll