import requests
from typing import Dict, Any, Optional
from app.core import get_settings

class GroqClient:
    def __init__(self):
        self.settings = get_settings()
        self.headers = {
            "Authorization": f"Bearer {self.settings.GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        self.base_url = self.settings.GROQ_URL

    async def get_response(
        self,
        user_input: str,
        conversation_id: Optional[str] = None,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        payload = {
            "inputs": {},
            "query": user_input,
            "conversation_id": conversation_id,
            "user": user_id,
            "files": []
        }

        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Error communicating with Groq API: {str(e)}")

groq_client = GroqClient() 