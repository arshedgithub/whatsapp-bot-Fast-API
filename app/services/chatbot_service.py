from typing import Dict, Optional
from app.integrations.groq_client import groq_client

class ChatbotService:
    def __init__(self):
        self.user_sessions: Dict[str, str] = {}

    async def process_message(self, user_id: str, message: str) -> str:
        conversation_id = self.user_sessions.get(user_id)
        
        try:
            response = await groq_client.get_response(
                user_input=message,
                conversation_id=conversation_id,
                user_id=user_id
            )
            
            new_conversation_id = response.get("conversation_id")
            if new_conversation_id:
                self.user_sessions[user_id] = new_conversation_id
                
            return response.get("answer", "Sorry! I didn't understand that.")
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return "There was an error processing your message. Please try again later."

chatbot_service = ChatbotService() 