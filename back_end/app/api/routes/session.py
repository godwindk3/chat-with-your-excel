import os
import uuid
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.storage import find_file_by_id
from app.api.routes.analyze import build_agent_for_file
from app.services.session_store import (
    create_session_record,
    get_session_record,
    append_message,
    list_sessions,
    delete_session,
)


router = APIRouter(tags=["session"])


class CreateSessionRequest(BaseModel):
    fileId: str
    sheetName: str


class CreateSessionResponse(BaseModel):
    sessionId: str
    fileId: str
    sheetName: str
    createdAt: str


class AskRequest(BaseModel):
    question: str


class Message(BaseModel):
    role: str
    content: str
    timestamp: str


class HistoryResponse(BaseModel):
    sessionId: str
    fileId: str
    sheetName: str
    messages: List[Message]


@router.post("/session", response_model=CreateSessionResponse)
def create_session(req: CreateSessionRequest):
    file_path = find_file_by_id(req.fileId)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    session_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    create_session_record(session_id=session_id, file_id=req.fileId, sheet_name=req.sheetName, created_at=now)
    return CreateSessionResponse(sessionId=session_id, fileId=req.fileId, sheetName=req.sheetName, createdAt=now)


@router.get("/session/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    rec = get_session_record(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Session not found")
    return HistoryResponse(sessionId=session_id, fileId=rec["fileId"], sheetName=rec["sheetName"], messages=rec["messages"])


class SessionSummary(BaseModel):
    sessionId: str
    fileId: str
    sheetName: str
    createdAt: str
    messagesCount: int
    lastMessageAt: str


@router.get("/sessions", response_model=list[SessionSummary])
def list_all_sessions(fileId: str | None = None):
    return list_sessions(file_id=fileId)


@router.delete("/session/{session_id}")
def delete_session_endpoint(session_id: str):
    success = delete_session(session_id)
    if success:
        return {"message": "Session deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Session not found")


@router.post("/session/{session_id}/ask", response_model=Message)
def ask(session_id: str, req: AskRequest):
    rec = get_session_record(session_id)
    if not rec:
        raise HTTPException(status_code=404, detail="Session not found")

    file_id = rec["fileId"]
    sheet_name = rec["sheetName"]
    file_path = find_file_by_id(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")

    # Store user message first
    now = datetime.now(timezone.utc).isoformat()
    append_message(session_id, role="user", content=req.question, timestamp=now)

    # Run analysis
    agent = build_agent_for_file(file_path, sheet_name)
    try:
        response = agent.invoke(req.question)
        output = response.get("output") if isinstance(response, dict) else str(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

    now2 = datetime.now(timezone.utc).isoformat()
    append_message(session_id, role="assistant", content=output, timestamp=now2)
    return Message(role="assistant", content=output, timestamp=now2)


