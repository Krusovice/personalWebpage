import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SystemMetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "metrics_group"

        # Join group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try:
            received_message = json.loads(text_data)
            print(f"Received message from Kafka: {received_message}") #Print to console
            await self.send_metrics({
                'message': received_message,
            })
        except json.JSONDecodeError:
            print("Received invalid JSON from Kafka.")
            await self.send_metrics({
                'error': 'Invalid JSON received.'
            })
        except Exception as e:
            print(f"Error processing message from Kafka: {e}")
            await self.send_metrics({
                'error': f'An error occurred: {e}'
            })


    async def send_metrics(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
        }))
