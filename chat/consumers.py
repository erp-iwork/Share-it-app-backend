from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import Message, User
import json
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def new_message(self, data):

        sender, receiver, message = (
            data["sender"],
            data["receiver"],
            data["message"],
        )

        sender_user = User.objects.get(id=sender)

        receiver_user = User.objects.get(id=receiver)

        message = Message.objects.create(
            sender=sender_user, receiver=receiver_user, message=message
        )

        content = {
            "command": "new_message",
            "message": {
                "id": str(message.id),
                "is_read": False,
                "sender": str(message.sender.id),
                "receiver": str(message.receiver.id),
                "message": message.message,
                "timestamp": message.timestamp,
            },
        }
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": content}
        )

    commands = {
        "new_message": new_message,
    }

    async def connect(self):
        self.room_name = "room"
        self.room_group_name = "chat_" + self.room_name

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):

        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):

        # Receive message from WebSocket
        json_data = json.loads(text_data)
        await self.commands[json_data["command"]](self, json_data)

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps(message))
