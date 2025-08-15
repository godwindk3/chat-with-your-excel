# Backend - Excel & Document Analysis API

This backend provides APIs for:
- **Pandas Agent**: Upload and analyze Excel/CSV files using natural language
- **RAG System**: Upload and chat with documents (TXT, DOCX, PDF)

## Setup

1. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure GOOGLE_API_KEY** (one of the following):
   
   **Option A: Using .env file (recommended)**
   Create `.env` file in this folder:
   ```
   GOOGLE_API_KEY=YOUR_API_KEY
   ```
   
   **Option B: Environment variable**
   ```bash
   # PowerShell
   $env:GOOGLE_API_KEY="YOUR_API_KEY"
   
   # CMD
   set GOOGLE_API_KEY=YOUR_API_KEY
   ```

4. **Run server**
   ```bash
   python -m uvicorn app.main:app --reload
   # or
   python start_with_logs.py
   ```

## Environment Variables

- `GOOGLE_API_KEY`: **Required** - Google Gemini API key
- `FRONTEND_ORIGIN`: Optional CORS origin (default: http://localhost:5173)
- `STORAGE_DIR`: Optional storage path (default: ./storage)

## API Endpoints

### Pandas Agent (Excel/CSV Analysis)
- `POST /api/upload`: Upload Excel/CSV → `{ fileId, filename, sheetNames }`
- `POST /api/analyze`: Analyze data → `{ fileId, sheetName, question } → { output }`
- `POST /api/session`: Create analysis session
- `POST /api/session/{id}/ask`: Ask questions in session

### RAG System (Document Chat)
- `POST /api/rag/upload`: Upload TXT/DOCX/PDF → `{ fileId, filename, message }`
- `GET /api/rag/files`: List RAG documents → `[{ fileId, filename, size, uploadedAt, fileType }]`
- `DELETE /api/rag/file/{fileId}`: Delete RAG file and related sessions
- `POST /api/rag/session`: Create chat session → `{ sessionId, sessionName, fileId, filename }`
- `GET /api/rag/sessions`: List RAG sessions
- `POST /api/rag/session/{id}/ask`: Chat with document → `{ role, content, timestamp }`
- `GET /api/rag/session/{id}/messages`: Get session message history
- `DELETE /api/rag/session/{id}`: Delete RAG session

### File Management
- `GET /api/files`: List uploaded Excel files
- `DELETE /api/files/{fileId}`: Delete Excel file
- `GET /api/sessions`: List Excel analysis sessions  
- `DELETE /api/session/{sessionId}`: Delete Excel session

## Features

✅ **Excel/CSV Support**: Upload and analyze tabular data with pandas agent  
✅ **Document Chat**: Upload and chat with text documents using RAG  
✅ **Session Management**: Persistent chat sessions with message history  
✅ **Session Separation**: Isolated sessions for Excel vs RAG workflows
✅ **Vector Search**: Semantic search in documents using Google embeddings  
✅ **File Management**: Upload, list, and delete files with cascade cleanup
✅ **Smart Deletion**: Delete files automatically removes related sessions and vector data
✅ **Error Handling**: Retry logic for API quota limits and graceful error responses
✅ **Logging**: Comprehensive request/response logging with structured output

## File Structure

```
app/
├── main.py              # FastAPI application
├── core/
│   ├── config.py        # Configuration settings
│   └── logging_config.py # Logging setup
├── api/routes/
│   ├── upload.py        # File upload endpoints
│   ├── analyze.py       # Pandas analysis endpoints
│   ├── session.py       # Session management
│   ├── files.py         # File management
│   ├── rag.py           # RAG upload/query endpoints
│   └── rag_session.py   # RAG session management
└── services/
    ├── storage.py       # File storage utilities
    ├── preprocess.py    # Data preprocessing
    ├── session_store.py # Session persistence
    └── rag_service.py   # RAG processing service
```

## Supported File Types

**Pandas Agent:**
- `.xlsx`, `.xls` (Excel files)
- `.csv` (Comma-separated values)

**RAG System:**
- `.txt` (Text files)
- `.docx` (Word documents)  
- `.pdf` (PDF documents)