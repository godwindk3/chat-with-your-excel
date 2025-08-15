# Frontend - Excel & Document Analysis UI

React-based frontend for Excel analysis and RAG document chat with modern, responsive interface.

## Features

### 📊 **Excel Analysis Interface**
- File upload with drag & drop support
- Sheet selection and preview
- Natural language chat interface  
- Session management and history
- Data visualization and results display

### 🤖 **RAG Document Interface**  
- Document upload for .txt, .docx, .pdf files
- Existing file selection from storage
- Document chat with semantic search
- Session creation and management
- File deletion with confirmation

### 🎨 **UI/UX Features**
- Modern dark theme with smooth animations
- Responsive design for mobile/tablet
- Loading states and error handling
- Confirmation dialogs for destructive actions
- Real-time updates and state management

## Setup

1. **Install dependencies**
   ```bash
   npm install
   ```

2. **Configure environment** (optional)
   ```bash
   # Create .env.local if backend runs on different URL
   echo "VITE_API_BASE=http://localhost:8000/api" > .env.local
   ```

3. **Run development server**
   ```bash
   npm run dev
   ```

4. **Access application**
   - Frontend: http://localhost:5173
   - Make sure backend is running on http://localhost:8000

## Navigation

- `/` - Excel file upload and analysis
- `/chat` - Excel analysis chat interface  
- `/sessions` - Excel analysis session history
- `/files` - Excel file management
- `/rag` - RAG document upload and selection
- `/rag/chat` - RAG document chat interface
- `/rag/sessions` - RAG session management

## Configuration

### Environment Variables (.env.local)
- `VITE_API_BASE` - Backend API URL (default: http://localhost:8000/api)


