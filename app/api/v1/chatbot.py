from fastapi import APIRouter, Request
from app.services import ChatbotService
from app.integrations import twilio_client

chatbot_service = ChatbotService()

router = APIRouter()

@router.post("/whatsapp")
async def reply_whatsapp(request: Request):
    try:
        from_number, user_input = await twilio_client.parse_incoming_message(request)
        print("User input: ", user_input)

        response = await chatbot_service.process_message(from_number, user_input)
        print("Response: ", response)

        return twilio_client.create_response(response)

    except Exception as e:
        print("Error processing message:", str(e))
        return twilio_client.create_response(
            "Sorry, there was an error processing your message. Please try again later."
        )
        # option here to connect to a human
