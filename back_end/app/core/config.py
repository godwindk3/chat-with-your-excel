import os
from typing import List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()


class Settings(BaseModel):
    storage_dir: str = os.environ.get("STORAGE_DIR", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "storage")))
    cors_allow_origins: List[str] = [
        os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173"),
        os.environ.get("FRONTEND_ORIGIN_ALT", "http://localhost:3000"),
        "*",
    ]
    google_api_key: Optional[str] = os.environ.get("GOOGLE_API_KEY")


settings = Settings()

# Ensure storage directory exists
os.makedirs(settings.storage_dir, exist_ok=True)


