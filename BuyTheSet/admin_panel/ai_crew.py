import tiktoken
import time
from icecream import ic
from llama_index.llms.groq import Groq
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatSummaryMemoryBuffer


class AICrew:
    TOKEN_LIMIT = 5000
    MODEL_NAME = "llama3-70b-8192"

    def __init__(self, consumer) -> None:
        self.llm = Groq(api_key=consumer.api_key, model=self.MODEL_NAME)
        self.consumer = consumer
        
    def update_api_key(self, new_api_key: str) -> None:
        self.llm = Groq(api_key=new_api_key, model=self.MODEL_NAME)

    async def model_one(self):
        system_prompt = """
        Always reply in the most confusing way possible, but you should reply to the user's message.
        """
        prompt = self.create_memory_with_system_message(system_prompt)
        last_response = ""
        try:
            async for response in await self.llm.astream_chat(prompt):
                new_part = response.message.content[len(last_response):]
                ic(new_part)
                yield new_part
                last_response = response.message.content
        except Exception as e:
            ic("Error yielding chunks:", e)        

    def create_memory_with_system_message(self, system_content: str) -> list[ChatMessage]:
        self.consumer.memory = ChatSummaryMemoryBuffer.from_defaults(
            chat_history=self.consumer.chat_history.copy(),
            llm=self.llm,
            token_limit=self.TOKEN_LIMIT,
            tokenizer_fn=tiktoken.encoding_for_model("gpt-2").encode,
        )
        memory = self.consumer.memory.chat_store.store['chat_history']
        system_message = ChatMessage(role="system", content=system_content)
        memory.append(system_message)
        return memory
    