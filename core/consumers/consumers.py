import json
import asyncio
from concurrent.futures import ThreadPoolExecutor
from channels.generic.websocket import AsyncWebsocketConsumer
from core.models.chat_field.models import Message
from asgiref.sync import sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 加入聊天组
        await self.channel_layer.group_add('chat_group', self.channel_name)
        await self.accept()

        history_messages = await self.get_history_messages(limit=20)

        for message in history_messages:
            await self.send(text_data=json.dumps({
            'sender': message.sender,
            'content': message.content,
        }))

    async def disconnect(self, close_code):
        # 离开聊天组
        await self.channel_layer.group_discard('chat_group', self.channel_name)

    async def receive(self, text_data):
        # 接收到前端发送的消息后，广播给所有在线用户
        data = json.loads(text_data)
        sender = data['sender']
        content = data['content']

        # 保存消息到数据库
        message = await sync_to_async(Message.objects.create)(sender=sender, content=content)

        # 广播消息给所有在线用户
        await self.channel_layer.group_send(
            'chat_group',
            {
                'type': 'chat_message',
                'sender': message.sender,
                'content': message.content,
            }
        )

    async def chat_message(self, event):
        # 接收到广播消息后，发送给前端
        sender = event['sender']
        content = event['content']

        await self.send(text_data=json.dumps({
            'sender': sender,
            'content': content,
        }))

    async def get_history_messages(self, limit=20):
        total_records = await sync_to_async(Message.objects.all().count)()

        if total_records < limit:
            limit = total_records
    
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, lambda: list(Message.objects.all().iterator())[:limit])

    
    