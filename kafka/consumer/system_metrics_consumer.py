import asyncio
from kafka import KafkaConsumer
import redis
import json
import time
import psycopg2
import os
from utils.config import POSTGRES_CONFIG, KAFKA_CONFIG, REDIS_CONFIG



# Kafka Consumer
consumer = KafkaConsumer('system_metrics',**KAFKA_CONFIG)

conn = psycopg2.connect(**POSTGRES_CONFIG)
cursor = conn.cursor()

# Redis connection
r = redis.Redis(host=REDIS_CONFIG['host'], port=REDIS_CONFIG['port'])

while True:
    messages = consumer.poll(timeout_ms=2000)  # Poll Kafka every second
    if messages:
        for _, records in messages.items():
            for record in records:
                try:
                    data = json.loads(record.value.decode('utf-8'))
                    data["type"] = "realtime"  # Fixed syntax

                    # Insert into PostgreSQL
                    cursor.execute(
                        "INSERT INTO system_metrics_table (timestamp, cpu_usage, ram_usage) VALUES (%s, %s, %s)",
                        (data['timestamp'], data['cpu_usage'], data['ram_usage'])
                    )

                    # Publish to Redis
                    r.publish("metrics_group", json.dumps(data))

                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing JSON: {e}")
                except psycopg2.Error as e:
                    print(f"Database error: {e}")
                    conn.rollback()  # Rollback transaction if an error occurs

    conn.commit()  # Commit after processing all messages in batch
