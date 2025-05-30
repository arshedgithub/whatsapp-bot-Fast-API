from fastapi import APIRouter, Request
from twilio.twiml.messaging_response import MessagingResponse
from app.services import ChatbotService

chatbot_service = ChatbotService()

router = APIRouter()

@router.post("/whatsapp")
async def reply_whatsapp(request: Request):
    print("Testing whatsapp route")

    form_data = await request.form()
    from_number = form_data.get('From', '')
    user_input = form_data.get('Body', '').strip()

    print("User input: ", user_input)

    resp = MessagingResponse()
    msg = resp.message()

    try:
        response = await chatbot_service.process_message(from_number, user_input)
        print("Response: ", response)
        msg.body(response)
    except Exception as e:
        print("Error processing message:", str(e))
        msg.body("Sorry, there was an error processing your message. Please try again later.")

    return str(resp)