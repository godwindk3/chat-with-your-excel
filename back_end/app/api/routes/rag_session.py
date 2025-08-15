import os
import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from app.services.storage import find_file_by_id
from app.services.rag_service import get_rag_service
from app.services.session_store import (
    create_session, get_session_record, delete_session_record,
    get_all_sessions, append_message, get_session_messages
)
from app.core.config import settings

logger = logging.getLogger("app.api.routes.rag_session")

router = APIRouter(tags=["rag_session"])


class RAGSessionRequest(BaseModel):
    fileId: str
    sessionName: str


class RAGSessionResponse(BaseModel):
    sessionId: str
    sessionName: str
    fileId: str
    filename: str
    createdAt: str


class Message(BaseModel):
    role: str
    content: str
    timestamp: str


class RAGAskRequest(BaseModel):
    question: str


def is_rag_file(file_path: str) -> bool:
    """Check if file is supported by RAG"""
    return file_path.lower().endswith((".txt", ".docx", ".pdf"))


@router.post("/rag/session", response_model=RAGSessionResponse)
def create_rag_session(req: RAGSessionRequest):
    """Create a new RAG chat session for a document"""
    logger.info(f"💬 CREATE RAG SESSION REQUEST")
    logger.info(f"   File ID: {req.fileId}")
    logger.info(f"   Session name: {req.sessionName}")
    
    # Verify file exists and is RAG-compatible
    file_path = find_file_by_id(req.fileId)
    if not file_path:
        logger.error(f"   ❌ File not found: {req.fileId}")
        raise HTTPException(status_code=404, detail="File not found")
    
    if not is_rag_file(file_path):
        logger.error(f"   ❌ File not supported for RAG: {file_path}")
        raise HTTPException(
            status_code=400,
            detail="File type not supported for RAG. Use .txt, .docx, or .pdf files."
        )
    
    # Create session
    try:
        now = datetime.now(timezone.utc).isoformat()
        session_id = create_session(
            file_id=req.fileId,
            session_name=req.sessionName,
            created_at=now,
            session_type="rag"  # Mark as RAG session
        )
        
        filename = os.path.basename(file_path).split("_", 1)[1] if "_" in os.path.basename(file_path) else os.path.basename(file_path)
        
        logger.info(f"   ✅ RAG session created: {session_id}")
        
        return RAGSessionResponse(
            sessionId=session_id,
            sessionName=req.sessionName,
            fileId=req.fileId,
            filename=filename,
            createdAt=now
        )
        
    except Exception as e:
        logger.error(f"   ❌ Error creating session: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create session: {e}")


@router.get("/rag/sessions")
def list_rag_sessions():
    """List all RAG chat sessions"""
    try:
        from app.services.session_store import list_sessions
        
        # Get only RAG sessions using the session_type filter
        rag_sessions = list_sessions(session_type="rag")
        
        # Add filename info for each session
        for session in rag_sessions:
            file_path = find_file_by_id(session["fileId"])
            if file_path:
                session["filename"] = os.path.basename(file_path).split("_", 1)[1] if "_" in os.path.basename(file_path) else os.path.basename(file_path)
            else:
                session["filename"] = "File not found"
        
        logger.info(f"📋 Listed {len(rag_sessions)} RAG sessions")
        return rag_sessions
        
    except Exception as e:
        logger.error(f"❌ Error listing RAG sessions: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to list sessions: {e}")


@router.get("/rag/session/{session_id}")
def get_rag_session(session_id: str):
    """Get a specific RAG session details"""
    rec = get_session_record(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify it's a RAG session by sessionType
    session_type = rec.get("sessionType", "pandas")
    if session_type != "rag":
        raise HTTPException(status_code=400, detail="Not a RAG session")
    
    # Also verify file type for double check
    file_path = find_file_by_id(rec["fileId"])
    if not file_path or not is_rag_file(file_path):
        raise HTTPException(status_code=400, detail="Not a RAG compatible file")
    
    session_data = rec.copy()
    session_data["filename"] = os.path.basename(file_path).split("_", 1)[1] if "_" in os.path.basename(file_path) else os.path.basename(file_path)
    
    return session_data


@router.get("/rag/session/{session_id}/messages")
def get_rag_session_messages(session_id: str) -> List[Message]:
    """Get all messages in a RAG session"""
    rec = get_session_record(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify it's a RAG session by sessionType
    session_type = rec.get("sessionType", "pandas")
    if session_type != "rag":
        raise HTTPException(status_code=400, detail="Not a RAG session")
    
    messages = get_session_messages(session_id)
    return [Message(**msg) for msg in messages]


@router.delete("/rag/session/{session_id}")
def delete_rag_session(session_id: str):
    """Delete a RAG session"""
    rec = get_session_record(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Verify it's a RAG session by sessionType
    session_type = rec.get("sessionType", "pandas")
    if session_type != "rag":
        raise HTTPException(status_code=400, detail="Not a RAG session")
    
    success = delete_session_record(session_id)
    if success:
        logger.info(f"🗑️ RAG session deleted: {session_id}")
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/rag/session/{session_id}/ask", response_model=Message)
async def ask_rag_document(session_id: str, req: RAGAskRequest):
    """Ask a question to a RAG document in a session"""
    import time
    
    logger.info(f"🤖 RAG ASK REQUEST")
    logger.info(f"   Session ID: {session_id}")
    logger.info(f"   Question: {req.question}")
    
    # Get session record
    rec = get_session_record(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Session not found")

    # Verify it's a RAG session by sessionType
    session_type = rec.get("sessionType", "pandas")
    if session_type != "rag":
        raise HTTPException(status_code=400, detail="Not a RAG session")

    file_id = rec["fileId"]
    file_path = find_file_by_id(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    
    if not is_rag_file(file_path):
        raise HTTPException(status_code=400, detail="Not a RAG compatible file")

    # Store user message first
    now = datetime.now(timezone.utc).isoformat()
    append_message(session_id, role="user", content=req.question, timestamp=now)

    # Query the document using RAG
    try:
        load_dotenv()
        google_api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise HTTPException(
                status_code=500, 
                detail="GOOGLE_API_KEY is not configured"
            )
        
        rag_service = get_rag_service(google_api_key)
        
        # Retry logic for quota exceeded errors
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Run RAG query in thread pool to avoid event loop issues
                import asyncio
                import concurrent.futures
                
                def _sync_query():
                    return rag_service.query_document(file_id, req.question)
                
                # Run in thread pool executor
                loop = asyncio.get_event_loop()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    answer = await loop.run_in_executor(executor, _sync_query)
                break
            except Exception as e:
                error_msg = str(e).lower()
                
                if "quota" in error_msg or "429" in error_msg or "resourceexhausted" in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = 10 * (attempt + 1)
                        logger.warning(f"   ⏳ Quota exceeded, retrying in {wait_time}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        raise HTTPException(
                            status_code=429, 
                            detail="Google API quota exceeded. Please wait and try again."
                        )
                else:
                    raise HTTPException(status_code=500, detail=f"Query failed: {e}")
        
        # Store assistant response
        now2 = datetime.now(timezone.utc).isoformat()
        append_message(session_id, role="assistant", content=answer, timestamp=now2)
        
        logger.info(f"   ✅ RAG query completed successfully")
        return Message(role="assistant", content=answer, timestamp=now2)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"   ❌ RAG query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
