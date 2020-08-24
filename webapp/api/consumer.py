import json

from channels.generic.websocket import AsyncWebsocketConsumer


class HealthRecordConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
         # Called with either text_data or bytes_data for each frame
        # You can call:
        await self.send(text_data=json.dumps(text_data))
        # Or, to send a binary frame:
        # await self.send(bytes_data="Hello world!")

    async def disconnect(self, close_code):
        # Called when the socket closes
        await self.close()
