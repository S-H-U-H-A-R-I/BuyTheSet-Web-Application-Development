from channels.db import database_sync_to_async
from icecream import ic
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from typing import List

class ChatDBOperations:
    
    def get_aichat_model(self):
        from .models import AIChat
        return AIChat
    
    def get_chatmessages_model(self):
        from .models import ChatMessages
        return ChatMessages
    
    def __init__(self, user_id: int, aichat_id: int, message_id: int):
        self.user_id = user_id
        self.aichat_id = aichat_id
        self.message_id = message_id
    
    @database_sync_to_async
    def get_api_key(self) -> str:
        api_key = self.get_aichat_model().objects.get(id=self.aichat_id).api_key
        return api_key
    
    @database_sync_to_async
    def get_system_message(self) -> str:
        """
        Get the system message from the database
        """
        try:
            ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
            conversation = ai_chat.messages.get(id=self.message_id)
            if conversation.system_message:
                return conversation.system_message
            else:
                return ""
        except Exception as e:
            ic("Get System Message: ", e)
            
            
    @database_sync_to_async
    def create_chat_message(self) -> int:
        try:
            ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
            new_message = self.get_chatmessages_model().objects.create(chat=ai_chat)
            return new_message.id
        except Exception as e:
            ic(f"Error creating new chat message: {e}")
            raise
        
    @database_sync_to_async
    def get_chat_message(self, message_id: int) -> BaseMessage:
        try:
            ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
            message = ai_chat.messages.get(id=message_id)
            return message
        except Exception as e:
            ic(f"Error getting chat message: {e}")
            raise
            

    @database_sync_to_async
    def save_chat_message(self, messages: List[BaseMessage]) -> None:
        try:
            ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
            conversation = ai_chat.messages.get(id=self.message_id)
            chat_history = []
            for message in messages:
                message_dict = {
                    "type": message.__class__.__name__,
                    "content": message.content,
                }
                chat_history.append(message_dict)
            conversation.chat_history = chat_history
            conversation.save()
        except Exception as e:
            ic(f"Error saving chat message: {e}")
            raise
        
    
    @database_sync_to_async
    def save_chat_system_message(self, chat_id: str, system_message: str) -> None:
        try:
            ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
            conversation = ai_chat.messages.get(id=chat_id)
            conversation.system_message = system_message
            conversation.save()
        except Exception as e:
            ic(f"Error saving system message: {e}")
            raise

        
    @database_sync_to_async
    def delete_chat_message(self, message_id: int) -> None:
        try:
            ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
            conversation = ai_chat.messages.get(id=message_id)
            conversation.delete()
        except Exception as e:
            ic(f"Error deleting chat message: {e}")
            raise
        

    @database_sync_to_async
    def save_api_key(self, api_key: str) -> None:
        ai_chat = self.get_aichat_model().objects.get(user_id=self.user_id)
        ai_chat.api_key = api_key
        ai_chat.save()
                