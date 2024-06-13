import tiktoken
from collections import deque
from icecream import ic
from llama_index.llms.groq import Groq
from llama_index.core.memory import ChatSummaryMemoryBuffer
from llama_index.core.llms import ChatMessage
from transformers import RagTokenizer, RagRetriever, RagTokenForGeneration
from .chatbot import Chatbot
from .chat_db_operations import ChatDBOperations


class ChatMessageHandler:
    MAX_CONVERSATIONS = 5
    
    def __init__(self, consumer):
        self.consumer = consumer

    async def handle_chat_message(self, content: dict) -> None:
        """
        This fucntion invokes the language model with the message from the content,
        sends a response back to the client, saves the chat message to the database,
        and extracts important information from the chat response.

        Args:
            content (dict): The content of the message.
        """
        await self._handle_chat_history(content['text'], 'user')
        model_one_response = ""
        async for response_chunk in self.consumer.ai_crew.model_one():
            model_one_response += response_chunk
            await self.consumer.send_message('chat_message', {'text': response_chunk})
        ic(model_one_response)
        await self._handle_chat_history(model_one_response, 'assistant')

    async def handle_chat_menu(self, content: dict) -> None:
        """
        Depending on the action specified in the content,
        this function performs different operations such as deleting a chat message,
        creating a new chat message, and setting up the chatbot.
        
        Args:
            content (dict): The content of the message.
        """
        action = content.get('action')
        if action == 'delete':
            await self._handle_delete_action(content)
        elif action == 'view':
            await self._handle_view_action(content)
        elif action == 'edit':
            await self._handle_edit_action(content)
        else:
            ic(f"Unknown action: {action}")
                
    async def handle_chat_settings(self, content: dict) -> None:
        """
        This function validates the API key specified in the content, sets up the chatbot with the API key,
        and saves the API key to the database.
        
        Args:
            content (dict): The content of the message.
        """
        if await self.consumer.validate_api_key(content['api_key']):
            try:
                self.consumer.api_key = content['api_key']
                self.consumer.ai_crew.update_api_key(content['api_key'])
                await self.consumer.db_operations.save_api_key(content['api_key'])
            except Exception as e:
                ic(e)
                await self.consumer.send_message('chat_settings', {'status': 'error', 'error_message': 'Problem saving Api key'})

    async def _handle_chat_history(self, message: str, role: str) -> None:
        """
        This function adds a new message to the consumer's chat history
        and ensures that the chat history does not exceed the maximum number of conversations.
        If the maximum number of conversations is exceeded, the oldest conversation is removed from the chat history.
        
        Args:
            message (str): The message to add to the chat history.
            role (str): The role of the message. Can be 'user' or 'assistant'.
        """
        if not isinstance(self.consumer.chat_history, deque):
            self.consumer.chat_history = deque(self.consumer.chat_history, maxlen=self.MAX_CONVERSATIONS*2)
        chat_message = ChatMessage(role=role, content=message)
        self.consumer.chat_history.append(chat_message)
        self.consumer.conversation_count = len(self.consumer.chat_history) // 2
    
    async def _handle_delete_action(self, content: dict) -> None:
        await self.consumer.db_operations.delete_chat_message(content['id'])
        self.consumer.message_id = await self.consumer.db_operations.create_chat_message()
        self.consumer.db_operations = ChatDBOperations(self.consumer.user_id, self.consumer.aichat_id, self.consumer.message_id)
        chat_history = await self.consumer.db_operations.get_session_history()
        self.consumer.conversation_memory.chat_memory = chat_history
    
    async def _handle_view_action(self, content: dict) -> None:
        chat_message = await self.consumer.db_operations.get_chat_message(content['id'])
        chat_message_dict = { 
            'id': str(chat_message.id), 
            'system_message': chat_message.system_message, 
            'created_at': chat_message.created_at.strftime('%Y-%m-%d') 
        }
        await self.consumer.send_message('chat_menu', {'action': 'view', 'content': chat_message_dict})
    
    async def _handle_edit_action(self, content: dict) -> None:
        await self.consumer.db_operations.save_chat_system_message(content['id'], content['system_message'])