import requests
from typing import Dict, Any, Optional
from app.core.config import get_settings

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
            # "model": "mixtral-8x7b-32768-v2",
            "model": "llama3-8b-8192",
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful WhatsApp assistant."
                },
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            "temperature": 0.7,
            "max_tokens": 1024,
            "top_p": 1,
            "stream": False
        }

        try:
            print("Sending request to Groq API with payload:", payload)
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            print("Received response from Groq API:", data)
            
            # Extract the response text from Groq's response format
            answer = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {
                "answer": answer,
                "conversation_id": conversation_id
            }
        except Exception as e:
            print(f"Error details: {str(e)}")
            if hasattr(e, 'response'):
                print(f"Response content: {e.response.text}")
            raise Exception(f"Error communicating with Groq API: {str(e)}")

groq_client = GroqClient() 