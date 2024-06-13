import json
import time
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from channels.exceptions import DenyConnection
from django.db import close_old_connections
from icecream import ic
from .chat_db_operations import ChatDBOperations
from .chatbot import Chatbot
from .chat_message_handlers import ChatMessageHandler
from .ai_crew import AICrew


class ChatConsumer(AsyncJsonWebsocketConsumer):
    def get_aichat_model(self):
        from .models import AIChat
        return AIChat
        
    def get_chatmessages_model(self):
        from .models import ChatMessages
        return ChatMessages
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ai_chat = None
        self.aichat_id = None
        self.user_id = None
        self.message_id = None
        self.chat_group_name = None
        self.api_key = None
        self.db_operations = None
        self.message_handler = None
        self.ai_crew = None
        self.chat_history = []
        self.memory = None
        self.conversation_count = 0
    
    async def connect(self) -> None:
        try:
            await self.initialize_user_and_chat()
            await self.initialize_latest_message()
            await self.initialize_chat_group()
            await self.initialize_db_operations()
            await self.initialize_api_key()
            await self.initialize_message_handler()
            await self.initialize_ai_crew()
            await self.accept()
            if self.api_key == None:
                await self.send_message('chat_settings', {'status': 'error', 'error_message': 'No API key'})
        except Exception as e:
            ic(f"Error connecting: {e}")
            await self.close()
    
    async def receive_json(self, content) -> None:
        message_type_handlers = {
            'chat_message': self.message_handler.handle_chat_message,
            'chat_menu': self.message_handler.handle_chat_menu,
            'chat_settings': self.message_handler.handle_chat_settings,
        }
        try:
            handler = message_type_handlers[content['type']]
        except Exception as e:
            ic(f"Unknown message type: {content['type']}")
        else:
            try:
                await handler(content)
            except Exception as e:
                ic(f"Error handling message: {e}")
                
    async def disconnect(self, close_code) -> None:
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)
        ic(close_code)
        close_old_connections()
        
    async def initialize_user_and_chat(self):
        user = self.scope['user']
        self.user_id = user.id
        self.ai_chat = await database_sync_to_async(self.get_aichat_model().objects.get)(user_id=self.user_id)
        self.aichat_id = self.ai_chat.id

    async def initialize_latest_message(self):
        try:
            latest_message = await database_sync_to_async(self.ai_chat.messages.last)()
            if latest_message is None:
                latest_message, created = await database_sync_to_async(self.get_chatmessages_model().objects.get_or_create)(chat=self.ai_chat)
            self.message_id = latest_message.id
        except Exception as e:
            ic(f"Error getting latest message: {e}")
            raise DenyConnection(str(e))

    async def initialize_chat_group(self):
        self.chat_group_name = f'chat_{self.aichat_id}'
        await self.channel_layer.group_add(self.chat_group_name, self.channel_name)

    async def initialize_db_operations(self):
        self.db_operations = ChatDBOperations(self.user_id, self.aichat_id, self.message_id)
        
    async def initialize_api_key(self):
        if await self.db_operations.get_api_key() != '':
            self.api_key = await self.db_operations.get_api_key()
        ...

    async def initialize_message_handler(self):
        self.message_handler = ChatMessageHandler(self)
        
    async def initialize_ai_crew(self):
        self.ai_crew = AICrew(self)
            
    async def send_message(self, type, content) -> None:
        await self.send(text_data=json.dumps({'type': type, **content}))

    async def validate_api_key(self, api_key) -> bool:
        try:
            if api_key != '':
                is_valid = await Chatbot._validate_api_key(api_key)
                if is_valid:
                    await self.send_message('chat_settings', {'status': 'success', 'success_message': 'Valid API key'})
                    return True
            await self.send_message('chat_settings', {'status': 'error', 'error_message': 'Invalid API key'})
            return False
        except:
            await self.send_message('chat_settings', {'status': 'error', 'error_message': 'Problem validating API key'})
            return False

    async def extract_important_information_from_chat(self, content) -> None:
        try:
            important_info = await Chatbot.extract_important_information(self.api_key, content['human_input'], content['text'])
            return important_info
        except Exception as e:
            ic(f"Error extracting important information: {e}")
            raise
        

    
        