import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import MessageChat

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
        message = text_data_json["message"]
        id_author = self.scope['session']['id']  

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, 
            {
                "type": "chat_message",
                "message": message,
                "id_author": id_author
            }
        )

    
    async def chat_message(self, event):
        message = event["message"]
        id_author = event['id_author']

        session_id = self.scope["session"].get('id')

        if id_author == session_id:
            await self.save_message(chat_name=self.room_name, id_author=session_id, message=message)
            

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message, 
            'id_author': id_author
        }))


    @database_sync_to_async
    def save_message(self, chat_name, id_author, message):

        message = MessageChat(chat=chat_name, id_author=id_author, message=message)
        message.save()