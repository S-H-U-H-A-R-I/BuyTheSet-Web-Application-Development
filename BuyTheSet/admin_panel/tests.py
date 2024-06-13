import tiktoken
from icecream import ic
from llama_index.core import VectorStoreIndex
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import ChatSummaryMemoryBuffer
from llama_index.llms.groq import Groq
from .models import ChatMessages

# def main():
#     chat_history = []
#     while True:
#         llm = Groq(api_key="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", model="llama3-70b-8192")
#         tokenizer_fn = tiktoken.encoding_for_model("gpt-2").encode
#         memory = ChatSummaryMemoryBuffer.from_defaults(
#             chat_history=chat_history,
#             llm=llm,
#             token_limit=5000,
#             tokenizer_fn=tokenizer_fn,
#         )
#         try:
#             user_input = input("Enter your message: ")
#             user_message = ChatMessage(role="user", content=user_input)
#             chat_history.append(user_message)
#         except Exception as e:
#             ic(f"Error getting user input: {e}")
#             break
#         try:
#             ic(memory.chat_store.store['chat_history'])
#             resp = llm.chat(memory.chat_store.store['chat_history'])
#             try:
#                 assistant_message = ChatMessage(role="assistant", content=resp.message.content)
#                 chat_history.append(assistant_message)
#             except Exception as e:
#                 ic(f"Error appending assistant message to chat history: {e}")
#                 break
#             ic(resp.message)
#         except Exception as e:
#             ic(f"Error getting assistant response: {e}")
#             break
    
# if __name__ == "__main__":
#     main()


def chat_message_to_dict(chat_message):
    return {
        'role': chat_message.role,
        'content': chat_message.content,
    }


def main():
    chat_history = []
    while True:
        llm = Groq(api_key="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", model="llama3-70b-8192")
        tokenizer_fn = tiktoken.encoding_for_model("gpt-2").encode
        memory = ChatSummaryMemoryBuffer.from_defaults(
            chat_history=chat_history,
            llm=llm,
            token_limit=5000,
            tokenizer_fn=tokenizer_fn,
        )
        try:
            user_input = input("Enter your message: ")
            user_message = ChatMessage(role="user", content=user_input)
            chat_history.append(user_message)
        except Exception as e:
            ic(f"Error getting user input: {e}")
            break
        try:
            ic(memory.chat_store.store['chat_history'])
            resp = llm.chat(memory.chat_store.store['chat_history'])
            try:
                assistant_message = ChatMessage(role="assistant", content=resp.message.content)
                chat_history.append(assistant_message)
            except Exception as e:
                ic(f"Error appending assistant message to chat history: {e}")
                break
            ic(chat_history)
        except Exception as e:
            ic(f"Error getting assistant response: {e}")
            break
        try:
            chat_history_dict = [chat_message_to_dict(message) for message in chat_history]
            ic(chat_history_dict)
            try:
                chat_messages = ChatMessages(chat_history=chat_history_dict)
                chat_messages.save()
            except Exception as e:
                ic(f"Error saving chat history to database: {e}")
                break
        except Exception as e:
            ic(f"Error converting chat history to dict: {e}")
            break
    
if __name__ == "__main__":
    main()


