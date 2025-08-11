import json
import os
from typing import Any, Dict, Optional, List

from app.core.config import settings


def _session_path(session_id: str) -> str:
    return os.path.join(settings.storage_dir, f"session_{session_id}.json")


def create_session_record(session_id: str, file_id: str, sheet_name: str, created_at: str) -> None:
    record = {
        "sessionId": session_id,
        "fileId": file_id,
        "sheetName": sheet_name,
        "createdAt": created_at,
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


def append_message(session_id: str, role: str, content: str, timestamp: str) -> None:
    path = _session_path(session_id)
    rec = get_session_record(session_id)
    if rec is None:
        return
    rec.setdefault("messages", []).append({
        "role": role,
        "content": content,
        "timestamp": timestamp,
    })
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rec, f, ensure_ascii=False, indent=2)


def list_sessions(file_id: Optional[str] = None) -> List[Dict[str, Any]]:
    sessions: List[Dict[str, Any]] = []
    try:
        for name in os.listdir(settings.storage_dir):
            if not name.startswith("session_") or not name.endswith(".json"):
                continue
            path = os.path.join(settings.storage_dir, name)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    rec = json.load(f)
                    if file_id and rec.get("fileId") != file_id:
                        continue
                    sessions.append({
                        "sessionId": rec.get("sessionId"),
                        "fileId": rec.get("fileId"),
                        "sheetName": rec.get("sheetName"),
                        "createdAt": rec.get("createdAt"),
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


