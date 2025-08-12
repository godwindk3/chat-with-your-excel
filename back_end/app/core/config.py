import os
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()


class Settings(BaseModel):
    storage_dir: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage"))
    
    # CORS configuration - filter out empty strings
    _cors_origins = [
        os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173"),
        os.environ.get("FRONTEND_ORIGIN_ALT", "http://localhost:3000"),
        os.environ.get("NGROK_ORIGIN", ""),  # For ngrok tunneling
    ]
    cors_allow_origins: List[str] = [origin for origin in _cors_origins if origin.strip()]
    
    google_api_key: Optional[str] = os.environ.get("GOOGLE_API_KEY")


settings = Settings()

# Ensure storage directory exists
os.makedirs(settings.storage_dir, exist_ok=True)


