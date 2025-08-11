# Excel Analysis Chat App

A web application for analyzing Excel files using AI chat interface. Upload Excel files, select sheets, and ask questions about your data using natural language.

## Features

- 📊 **Excel File Analysis**: Upload and analyze .xlsx/.xls files
- 💬 **Chat Interface**: Ask questions about your data in natural language
- 📝 **Session Management**: Save and continue conversations
- 📁 **File Management**: Reuse uploaded files from storage
- 🔄 **Sheet Selection**: Choose specific sheets to analyze
- 🗂️ **Smart Preprocessing**: Automatic data type detection and cleaning

## Tech Stack

- **Backend**: FastAPI, pandas, LangChain, Google Gemini AI
- **Frontend**: React, TypeScript, Vite
- **Storage**: Local file system for Excel files and chat sessions

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

1. **Upload Files**: 
   - Go to Upload page or use Chat sidebar
   - Upload new Excel files or select from storage

2. **Start Chat Session**:
   - Select a sheet from your Excel file
   - Click "Start Session" to begin analysis

3. **Ask Questions**:
   - Type questions about your data in natural language
   - Examples: "What are the top 5 sales regions?", "Show me monthly trends"

4. **Manage Sessions**:
   - View past conversations in Sessions page
   - Continue previous chats by clicking on session history
   - Delete sessions you no longer need

5. **File Management**:
   - View all uploaded files in Files page
   - Delete files to free up storage space

## API Endpoints

- `POST /api/upload` - Upload Excel file
- `GET /api/files` - List uploaded files  
- `GET /api/files/{id}/info` - Get file info with sheet names
- `DELETE /api/files/{id}` - Delete file
- `POST /api/session` - Create chat session
- `GET /api/sessions` - List chat sessions
- `POST /api/session/{id}/ask` - Send question
- `DELETE /api/session/{id}` - Delete session

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
- Only .xlsx and .xls files are supported
- Check file permissions and storage directory
- Ensure files are not corrupted

## License

This project is open source and available under the MIT License.

