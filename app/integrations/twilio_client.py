from twilio.twiml.messaging_response import MessagingResponse
from fastapi import Request
from fastapi.responses import Response
from typing import Tuple

class TwilioClient:
    @staticmethod
    async def parse_incoming_message(request: Request) -> Tuple[str, str]:
        """Parse incoming WhatsApp message from Twilio request."""
        form_data = await request.form()
        from_number = form_data.get('From', '')
        user_input = form_data.get('Body', '').strip()
        return from_number, user_input

    @staticmethod
    def create_response(message: str) -> Response:
        """Create a TwiML response for WhatsApp."""
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(message)
        return Response(content=str(resp), media_type="application/xml")

twilio_client = TwilioClient() 