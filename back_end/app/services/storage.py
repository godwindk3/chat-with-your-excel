import os
from typing import Optional, List, Dict, Any

from app.core.config import settings


def list_storage_files() -> list[str]:
    try:
        return [os.path.join(settings.storage_dir, f) for f in os.listdir(settings.storage_dir)]
    except FileNotFoundError:
        return []


def find_file_by_id(file_id: str) -> Optional[str]:
    prefix = f"{file_id}_"
    
    # Direct approach - check storage directory
    try:
        files = os.listdir(settings.storage_dir)
        for filename in files:
            if filename.startswith(prefix) and filename.endswith((".xlsx", ".xls")):
                full_path = os.path.join(settings.storage_dir, filename)
                if os.path.exists(full_path):
                    return full_path
    except Exception:
        pass
    
    # Fallback to original method
    for path in list_storage_files():
        if os.path.basename(path).startswith(prefix):
            return path
    return None


def list_uploaded_files() -> List[Dict[str, Any]]:
    files = []
    try:
        for name in os.listdir(settings.storage_dir):
            if name.startswith("session_") or not ("_" in name and name.endswith((".xlsx", ".xls"))):
                continue
            path = os.path.join(settings.storage_dir, name)
            try:
                stat = os.stat(path)
                # Extract file_id and original name
                parts = name.split("_", 1)
                if len(parts) >= 2:
                    file_id = parts[0]
                    original_name = parts[1]
                    files.append({
                        "fileId": file_id,
                        "filename": original_name,
                        "size": stat.st_size,
                        "uploadedAt": stat.st_mtime,
                        "path": path
                    })
            except Exception:
                continue
        # Sort by upload time desc
        files.sort(key=lambda f: f["uploadedAt"], reverse=True)
    except FileNotFoundError:
        pass
    return files


def delete_file_by_id(file_id: str) -> bool:
    file_path = find_file_by_id(file_id)
    if file_path and os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception:
            return False
    return False


