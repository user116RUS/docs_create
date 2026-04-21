import os
import base64

import dotenv
from openai import OpenAI

dotenv.load_dotenv()

PROMPT = """
You are a precise OCR and data extraction AI for a document management system. 
Analyze the provided image of an organization/business card (partner map) and extract the information into a strictly formatted JSON object.

EXTRACT THESE FIELDS (use exact JSON keys):
- "name": Full legal name of the organization, ideally in the format "Organization Name, represented by Position Head_FullName". (e.g. "ООО «Алга», в лице директора Иванова И.И.")
- "short_name": Short name or abbreviation (e.g. "ООО «Алга»")
- "fio": Full name of the head/manager (e.g. "Иванов Иван Иванович")
- "function": Official title of the head. MUST BE strictly either "Директор" or "Индивидуальный предприниматель".
- "inn": Taxpayer Identification Number (ИНН) - digits only.
- "kpp": Tax Registration Reason Code (КПП) - digits only. Dont confuse with "ОГРН" or "ОГРНИП" or any other digits.
- "address": Complete physical address or office address. If there's no any - legal address.
- "bank_name": Full name of the bank.
- "bik": Bank Identification Code (БИК) - digits only.
- "bank_account": Settlement account number (Р/С) - digits only.
- "correspondent_bank_account": Correspondent account number (К/С) - digits only.
- "requisites": A structured text block containing all organization details formatted for copy-pasting.

STRICT RULES:
1. Extract ONLY text clearly visible in the image.
2. Output MUST be in Russian as it appears on the document.
3. If a field is missing or unreadable, leave as "".
4. NO markdown formatting, NO ```json blocks, NO explanations. Return ONLY the raw JSON object. Even if it's not the partner map, return the JSON object.
5. Don't confuse the data (e.g. "ОГРНИП" and "КПП"). If you dont have any data, leave as ""!.
6. If you dont have any data, leave as ""!.
7. DO NOT RETURN NON-JSON FORMAT ANSWER.
8. DO NOT THINK UP ANY DATA

JSON OUTPUT TEMPLATE:
{
  "name": "",
  "short_name": "",
  "fio": "",
  "function": "",
  "inn": "",
  "kpp": "",
  "address": "",
  "bank_name": "",
  "bik": "",
  "bank_account": "",
  "correspondent_bank_account": "",
  "requisites": ""
}
"""

ASSISTANT_PROMPT = PROMPT
ORGANISATION_EXTRACTION_PROMPT = PROMPT
ANALYTIC_PROMPT = 'settings.ANALYTIC_PROMPT'


class BaseAIAPI:
    def __init__(self, ) -> None:
        self._ASSISTANT_PROMPT: str = ASSISTANT_PROMPT
        self.chat_history: dict = {}
        self._TEMPERATURE = 0.7
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.vsegpt.ru/v1"
        )

    def clear_chat_history(self, chat_id: int) -> None:
        self.chat_history.pop(chat_id)


class OpenAIAPI(BaseAIAPI):
    """API for working with https://vsegpt.ru/Docs/API"""

    def __init__(self, ) -> None:
        super().__init__()

    def _get_or_create_user_chat_history(self, chat_id: int, new_user_message: str = "") -> list:
        if not self.chat_history.get(chat_id, False):
            self.chat_history[chat_id] = []
            self.chat_history[chat_id].append({"role": "system", "content": self._ASSISTANT_PROMPT})
            self.chat_history[chat_id].append({"role": "user", "content": new_user_message})
            return self.chat_history[chat_id]

        self.chat_history[chat_id].append({"role": "user", "content": new_user_message})
        chat_history = self.chat_history[chat_id]
        return chat_history

    def get_response(self, chat_id: int, text: str, model: str, max_token: int =1024) -> dict:
        """
        Make request to AI and write answer to message_history.
        Usually working in chats with AI.
        """
        user_chat_history = self._get_or_create_user_chat_history(chat_id, text)

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=user_chat_history,
                temperature=self._TEMPERATURE,
                n=1,
                max_tokens=max_token,
            )

            answer = {"message": response.choices[0].message.content, "total_cost": getattr(response.usage, 'total_cost', 0)}
            self.chat_history[chat_id].append({"role": "assistant", "content": answer["message"]})

            return answer

        except Exception as e:
            print(f"Chat API Error: {e}")
            return None

    def add_txt_to_user_chat_history(self, chat_id: int, text: str) -> None:
        try:
            self._get_or_create_user_chat_history(chat_id, text)
        except Exception as e: 
            print("Error occurred while adding text to user chat history")

    def get_vision_response(self, text: str, base64_image: str, model: str, max_tokens: int = 3000) -> dict:
        """
        Get response from AI vision model using base64 encoded image.
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": text},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                },
                            },
                        ],
                    }
                ],
                max_tokens=max_tokens,
                extra_headers={"X-Title": "Organisation Vision Extractor"},
            )
            
            answer = {
                "message": response.choices[0].message.content,
                "total_cost": getattr(response.usage, 'total_cost', 0)
            }
            return answer
        except Exception as e:
            print(f"Vision API Error: {e}")
            return None

    def get_single_response(self, text: str, model: str, system_prompt: str = "") -> str:
        """
        Get single response without chat history.
        """
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": text})
            
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.2,
                max_tokens=3000,
                extra_headers={"X-Title": "Organisation Data Extractor"},
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Single Response API Error: {e}")
            return None