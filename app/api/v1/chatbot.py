from fastapi import APIRouter, Request
from twilio.twiml.messaging_response import MessagingResponse
from app.services.chatbot_service import chatbot_service

router = APIRouter()

@router.post("/whatsapp")
async def reply_whatsapp(request: Request):
    form_data = await request.form()
    from_number = form_data.get('From', '')
    user_input = form_data.get('Body', '').strip()

    resp = MessagingResponse()
    msg = resp.message()

    response = await chatbot_service.process_message(from_number, user_input)
    msg.body(response)

    return str(resp) 