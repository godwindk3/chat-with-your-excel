import json
import os
from typing import Any, Dict, Optional, List

from app.core.config import settings


def _session_path(session_id: str) -> str:
    return os.path.join(settings.storage_dir, f"session_{session_id}.json")


def create_session_record(session_id: str, file_id: str, sheet_name: str, created_at: str, session_type: str = "pandas") -> None:
    record = {
        "sessionId": session_id,
        "fileId": file_id,
        "sheetName": sheet_name,
        "createdAt": created_at,
        "sessionType": session_type,  # "pandas" or "rag"
        "messages": [],
    }
    with open(_session_path(session_id), "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)


def get_session_record(session_id: str) -> Optional[Dict[str, Any]]:
    path = _session_path(session_id)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def append_message(session_id: str, role: str, content: str, timestamp: str, trace: str | None = None) -> None:
    path = _session_path(session_id)
    rec = get_session_record(session_id)
    if rec is None:
        return
    message = {
        "role": role,
        "content": content,
        "timestamp": timestamp,
    }
    if trace:
        message["trace"] = trace
    rec.setdefault("messages", []).append(message)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)


def list_sessions(file_id: Optional[str] = None, session_type: Optional[str] = None) -> List[Dict[str, Any]]:
    sessions: List[Dict[str, Any]] = []
    try:
        for name in os.listdir(settings.storage_dir):
            if not name.startswith("session_") or not name.endswith(".json"):
                continue
            path = os.path.join(settings.storage_dir, name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    rec = json.load(f)
                    
                    # Filter by file_id if provided
                    if file_id and rec.get("fileId") != file_id:
                        continue
                    
                    # Filter by session_type if provided
                    rec_session_type = rec.get("sessionType", "pandas")  # default to pandas for backward compatibility
                    if session_type and rec_session_type != session_type:
                        continue
                    
                    sessions.append({
                        "sessionId": rec.get("sessionId"),
                        "fileId": rec.get("fileId"),
                        "sheetName": rec.get("sheetName"),
                        "createdAt": rec.get("createdAt"),
                        "sessionType": rec_session_type,
                        "messagesCount": len(rec.get("messages", [])),
                        "lastMessageAt": rec.get("messages", [])[-1]["timestamp"] if rec.get("messages") else rec.get("createdAt"),
                    })
            except Exception:
                continue
        # Sort by lastMessageAt desc
        sessions.sort(key=lambda r: r.get("lastMessageAt") or "", reverse=True)
    except FileNotFoundError:
        pass
    return sessions


def delete_session(session_id: str) -> bool:
    path = _session_path(session_id)
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        return False
    except Exception:
        return False


# Helper functions for the new session system
def create_session(file_id: str, session_name: str, created_at: str, session_type: str = "pandas") -> str:
    """Create a new session and return session ID"""
    import uuid
    session_id = str(uuid.uuid4())
    
    # For RAG sessions, we don't use sheet_name
    sheet_name = session_name if session_type == "rag" else session_name
    
    create_session_record(session_id, file_id, sheet_name, created_at, session_type)
    return session_id


def get_all_sessions() -> List[Dict[str, Any]]:
    """Get all sessions regardless of file"""
    return list_sessions()


def delete_session_record(session_id: str) -> bool:
    """Delete a session record"""
    return delete_session(session_id)


def get_session_messages(session_id: str) -> List[Dict[str, Any]]:
    """Get all messages for a session"""
    rec = get_session_record(session_id)
    if rec is None:
        return []
    return rec.get("messages", [])


