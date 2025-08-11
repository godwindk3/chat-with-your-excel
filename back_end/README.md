Run backend

1. Create and activate a virtual environment
2. pip install -r requirements.txt
3. Configure GOOGLE_API_KEY (one of the following):
   - Using .env file (recommended): create a file named `.env` in this folder with:
     
     GOOGLE_API_KEY=YOUR_API_KEY
     
     `.env` is automatically loaded on startup.
   - Or set environment variable directly (PowerShell):
     
     $env:GOOGLE_API_KEY="YOUR_API_KEY"
     
   - Or set environment variable directly (cmd):
     
     set GOOGLE_API_KEY=YOUR_API_KEY
     
4. Run server:
   
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

Environment variables

- GOOGLE_API_KEY: Required
- FRONTEND_ORIGIN: Optional CORS origin
- STORAGE_DIR: Optional storage path

API

- POST /api/upload: multipart form-data file -> { fileId, sheetNames }
- POST /api/analyze: { fileId, sheetName, question } -> { output }


