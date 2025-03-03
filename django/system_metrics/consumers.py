import json
import asyncio
import psycopg2
import redis
from datetime import datetime, timedelta
from channels.generic.websocket import AsyncWebsocketConsumer
from zoneinfo import ZoneInfo

class SystemMetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

        # Fetch the last hour of data from PostgreSQL
        history_data = self.get_last_hour_metrics()

        # Send initial data to the frontend
        await self.send(json.dumps({"data": history_data}))

        # Subscribe to Redis for real-time updates
        self.redis = redis.Redis(host="redis", port=6379, decode_responses=True)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe("metrics_group")

        await self.listen_to_redis()

    def get_last_hour_metrics(self):
        """Fetches the last hour of metrics from PostgreSQL."""
        try:
            conn = psycopg2.connect(
                dbname="personalWebpage_db",
                user="Krusovice",
                password="fedefrede",
                host="postgres_db",
                port="5432"
            )
            cursor = conn.cursor()

            one_hour_ago = datetime.now(ZoneInfo("Europe/Stockholm")) - timedelta(hours=1)
            query = """
                SELECT timestamp, cpu_usage, ram_usage
                FROM system_metrics_table
                WHERE timestamp >= %s
                ORDER BY timestamp ASC
            """
            cursor.execute(query, (one_hour_ago,))
            data = cursor.fetchall()
            cursor.close()
            conn.close()

            # Convert data to a list of dicts
            return [
                {"timestamp": row[0].isoformat(), "cpu_usage": row[1], "ram_usage": row[2], "type": "history"}
                for row in data
            ]
        except psycopg2.Error as e:
            print(f"Database error: {e}")
            return []

    async def listen_to_redis(self):
        """Continuously listens for real-time updates from Redis."""
        while True:
            message = self.pubsub.get_message()
            if message and message['type'] == 'message':
                await self.send(message['data'])
            await asyncio.sleep(1)  # Avoid busy-waiting

    async def disconnect(self, close_code):
        """Cleanup on disconnect."""
        self.pubsub.close()
        self.redis.close()
