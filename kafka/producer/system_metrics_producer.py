import psutil
import json
from datetime import datetime
import time
from kafka import KafkaProducer
from zoneinfo import ZoneInfo

# Kafka producer setup
producer = KafkaProducer(bootstrap_servers=['kafka:9092'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))

def monitor_system():
    cpu_usage = psutil.cpu_percent(interval=1)  # CPU usage in percentage
    ram_usage = psutil.virtual_memory().percent  # RAM usage in percentage
    data = {
        'cpu_usage': cpu_usage,
        'ram_usage': ram_usage,
        'timestamp': datetime.now(ZoneInfo("Europe/Stockholm")).strftime('%Y-%m-%d %H:%M:%S')
    }
    producer.send('system_metrics', value=data)
    print(f"Producer sent: {data}")  # Debugging info

if __name__ == "__main__":
    try:
        while True:
            monitor_system()
            time.sleep(1)  # Avoid overwhelming Kafka
    except KeyboardInterrupt:
        print("Stopping producer...")
        producer.flush()  # Ensure all messages are sent
        producer.close()