from fastapi import FastAPI
from app.core.config import get_settings
from app.api.v1 import chatbot

app = FastAPI(title=get_settings().APP_NAME)

# Include routers
app.include_router(chatbot.router, prefix="/api/v1")

@app.get('/')
def home():
    return 'WA-Bot Deployed Successfully!'
