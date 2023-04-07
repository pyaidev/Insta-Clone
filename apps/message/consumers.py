import json
from channels.generic.websocket import AsyncWebsocketConsumer
from apps.message.models import Message
from channels.db import database_sync_to_async
from datetime import datetime


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        send_data = await self.RecieveData(text_data_json)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'data': send_data['data']
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event['data']))

    async def RecieveData(self, data):
        if data['type'] == "send_message":
            data['data'] = await self.send_message(data)
        elif data['type'] == "get_typing":
            data['data'] = await self.get_typing(data)

        return data

    async def send_message(self, event):
        chat_id = event['data']["chat_id"]
        user_id = event['data']["user_id"]
        message = event['data']["message"]
        result, msg = await database_sync_to_async(self.add_message)(chat_id, user_id, message)

        data = {
            "type": event['type'],
            "data": {
                "chat_id": chat_id,
                "user_id": user_id,
                "message": message,
                "result": result,
                "created_at": datetime.now().strftime("%B %d, %Y, %I:%M %p")
                # "created_at": msg.created_at.strftime("%B %d, %Y, %I:%M %p")
            }
        }

        return data

    async def get_typing(self, event):

        data = {
            "type": "get_typing",
            "data": {
                "chat_id": event['data']["chat_id"],
                "user_id": event['data']["user_id"],
                "message": event['data']["message"]
            }

        }

        return data

    def add_message(self, chat_id, user_id, message):
        try:
            msg = Message.objects.create(chat_id=chat_id, sender_id=user_id, msg=message)
            return 'success', msg
        except Exception as e:
            return 'error', e
