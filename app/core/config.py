from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    GROQ_API_KEY: str
    GROQ_URL: str
    
    # Twilio Settings
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    
    # App Settings
    APP_NAME: str = "WhatsApp Bot"
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()
