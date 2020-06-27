from channels.generic.websocket import AsyncWebsocketConsumer
from main.models import Message, User
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def init_chat(self, data):
        email = data["email"]

        user = User.objects.get(email=email)

        content = {"command": "init_chat"}
        if not user:
            content["error"] = "Unable to get or create User with username : " + email
        content["success"] = "Chatting success with username : " + email
        await self.send(text_data=json.dumps(content))

    async def fetch_messages(self, data):
        messages = Message.objects.order_by("-timestamp").all()[:50]
        messages_list = []
        for message in messages:

            messages_list.append(
                {
                    "id": str(message.id),
                    "sender": message.sender.email,
                    "receiver": message.receiver.email,
                    "message": message.message,
                    "timestamp": str(message.timestamp),
                }
            )

        content = {"command": "messages", "messages": messages_list}
        await self.send(text_data=json.dumps(content))

    async def new_message(self, data):
        sender, receiver, message = (
            data["sender"],
            data["receiver"],
            data["message"],
        )

        sender_user = User.objects.get(email=sender)
        receiver_user = User.objects.get(email=receiver)

        message = Message.objects.create(
            sender=sender_user, receiver=receiver_user, message=message
        )

        content = {
            "command": "new_message",
            "message": {
                "id": str(message.id),
                "sender": message.sender.email,
                "receiver": message.receiver.email,
                "message": message.message,
                "timestamp": str(message.timestamp),
            },
        }
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": content}
        )

    commands = {
        "init_chat": init_chat,
        "fetch_messages": fetch_messages,
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
