from fastapi import FastAPI
import uvicorn
from app.core.config import get_settings
from app.api.v1 import router

app = FastAPI(title=get_settings().APP_NAME)

# Include routers
app.include_router(router, prefix="/api/v1")

@app.get('/')
def home():
    return 'WA-Bot Deployed Successfully!'

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
