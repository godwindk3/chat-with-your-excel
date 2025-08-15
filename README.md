# Excel & Document Analysis Chat App

A comprehensive web application for analyzing both Excel files and documents using AI chat interface. Features dual analysis modes: Excel/CSV analysis with pandas agent and document chat using RAG (Retrieval-Augmented Generation) technology.

## Features

### 📊 **Excel Analysis (Pandas Agent)**
- 📈 **Excel/CSV File Analysis**: Upload and analyze .xlsx/.xls/.csv files
- 💬 **Natural Language Queries**: Ask questions about your data
- 📝 **Session Management**: Save and continue analysis conversations
- 🔄 **Sheet Selection**: Choose specific sheets to analyze
- 🗂️ **Smart Preprocessing**: Automatic data type detection and cleaning

### 🤖 **Document Chat (RAG System)**
- 📄 **Document Upload**: Support for .txt, .docx, .pdf files
- 🧠 **Intelligent Chat**: Chat with your documents using RAG technology
- 🔍 **Semantic Search**: Find relevant information across document content
- 💾 **Session History**: Persistent chat sessions with documents
- 🗑️ **File Management**: Upload, select, and delete document files

## Tech Stack

- **Backend**: FastAPI, pandas, LangChain, Google Gemini AI
- **Frontend**: React, TypeScript, Vite
- **Storage**: Local file system for files and chat sessions
- **RAG**: Vector embeddings with Google Gemini for document analysis
- **Analytics**: Pandas agent for Excel/CSV data analysis

## Setup & Installation

### Prerequisites

- Python 3.8+ 
- Node.js 18+
- Google API Key (for Gemini AI)

### Backend Setup

1. Navigate to backend directory:
```bash
cd back_end
```

2. Create and activate virtual environment:
```bash
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# macOS/Linux  
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set environment variables:
```bash
# Create .env file
echo "GOOGLE_API_KEY=your_google_api_key_here" > .env

# Or set directly (Windows PowerShell)
$env:GOOGLE_API_KEY="your_google_api_key_here"

# Or set directly (macOS/Linux)
export GOOGLE_API_KEY="your_google_api_key_here"
```

5. Run backend server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd front_end
```

2. Install dependencies:
```bash
npm install
```

3. (Optional) Configure API endpoint:
```bash
# Create .env.local file if backend runs on different port
echo "VITE_API_BASE=http://localhost:8000/api" > .env.local
```

4. Run frontend development server:
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

## Usage

### 📊 **Excel Analysis Mode**

1. **Upload Excel Files**: 
   - Go to main Upload page
   - Upload new Excel/CSV files or select from storage

2. **Start Analysis Session**:
   - Select a sheet from your Excel file
   - Click "Start Session" to begin analysis

3. **Ask Questions**:
   - Type questions about your data in natural language
   - Examples: "What are the top 5 sales regions?", "Show me monthly trends"

### 🤖 **Document Chat Mode (RAG)**

1. **Upload Documents**:
   - Go to "RAG Upload" page
   - Upload .txt, .docx, .pdf files or choose from existing files

2. **Start Document Chat**:
   - Click "Start Chat" on any uploaded document
   - Create a new chat session with custom name

3. **Chat with Documents**:
   - Ask questions about document content
   - Examples: "What is the main topic?", "Summarize key points"

### 📝 **Session Management**

4. **Manage Sessions**:
   - View past conversations in respective Sessions pages
   - Continue previous chats by clicking on session history
   - Delete individual sessions or entire files with related sessions

5. **File Management**:
   - View all uploaded files in Files page
   - Delete files to free up storage space
   - Separate management for Excel files and RAG documents

## API Endpoints

### Excel Analysis APIs
- `POST /api/upload` - Upload Excel/CSV file
- `GET /api/files` - List uploaded Excel files  
- `GET /api/files/{id}/info` - Get file info with sheet names
- `DELETE /api/files/{id}` - Delete Excel file
- `POST /api/session` - Create Excel analysis session
- `GET /api/sessions` - List Excel analysis sessions
- `POST /api/session/{id}/ask` - Ask question about Excel data
- `DELETE /api/session/{id}` - Delete Excel session

### RAG Document APIs
- `POST /api/rag/upload` - Upload document (.txt, .docx, .pdf)
- `GET /api/rag/files` - List uploaded RAG documents
- `DELETE /api/rag/file/{id}` - Delete RAG document and related sessions
- `POST /api/rag/session` - Create RAG chat session
- `GET /api/rag/sessions` - List RAG chat sessions
- `POST /api/rag/session/{id}/ask` - Chat with document
- `GET /api/rag/session/{id}/messages` - Get session messages
- `DELETE /api/rag/session/{id}` - Delete RAG session

## Configuration

### Environment Variables

**Backend (.env)**:
- `GOOGLE_API_KEY` - Required for AI analysis
- `STORAGE_DIR` - File storage directory (optional)
- `FRONTEND_ORIGIN` - CORS origin (optional)

**Frontend (.env.local)**:
- `VITE_API_BASE` - Backend API URL (default: http://localhost:8000/api)

## Project Structure

```
chat-with-your-excel/
├── back_end/                 # FastAPI backend
│   ├── app/
│   │   ├── api/routes/      # API endpoints
│   │   ├── core/            # Configuration
│   │   └── services/        # Business logic
│   ├── storage/             # File storage (auto-created)
│   └── requirements.txt
│
├── front_end/               # React frontend  
│   ├── src/
│   │   ├── features/        # Feature components
│   │   ├── shared/          # Shared utilities
│   │   ├── ui/             # UI components
│   │   └── routes/         # Route configuration
│   └── package.json
│
└── back_end_test/          # Original test files
```

## Troubleshooting

**Backend Issues**:
- Ensure GOOGLE_API_KEY is set correctly
- Check Python version compatibility
- Verify all dependencies are installed

**Frontend Issues**:
- Clear browser cache and restart dev server
- Check if backend is running on correct port
- Verify Node.js version

**File Upload Issues**:
- Excel mode: Only .xlsx, .xls, .csv files are supported
- RAG mode: Only .txt, .docx, .pdf files are supported
- Check file permissions and storage directory
- Ensure files are not corrupted

## License

This project is open source and available under the MIT License.

