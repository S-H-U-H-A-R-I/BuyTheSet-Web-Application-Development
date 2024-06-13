import time
from groq import Groq
from icecream import ic


class Chatbot:

    @staticmethod
    async def _validate_api_key(api_key: str) -> bool:
        """
        Validates the provided API key by attempting to instantiate a Groq object and list its models.
        """
        try:
            if api_key != '':
                llm = Groq(api_key=api_key)
                response = llm.models.list()
                return response is not None
        except Exception as e:
            ic(f"Error validating API key: {e}")
            return False

    @staticmethod
    async def extract_important_information(api_key: str, human_input: str, assistant_response: str) -> str:
        try: 
            llm = Groq(api_key=api_key)
            system_message = (
                "Extract important information from the chat between the user and the assistant. Give only the extracted information. "
                "The user input will come first followed by the assistant's response, separated by a newline. "
                "If there is no important information, just output 'null'. No one will be seeing your output."
            )
            response = llm.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": human_input + "\n" + assistant_response},  
                ],
                model="llama3-70b-8192",
                temperature=0.5,
            )
            ic(response)
            return response.choices[0].message.content
        except Exception as e:
            ic(f"Error extracting important information: {e}")
            raise
        
        
    
        

