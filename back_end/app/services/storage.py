import os
import logging
from typing import Optional, List, Dict, Any

from app.core.config import settings

logger = logging.getLogger("app.services.storage")


def list_storage_files() -> list[str]:
    try:
        return [os.path.join(settings.storage_dir, f) for f in os.listdir(settings.storage_dir)]
    except FileNotFoundError:
        return []


def find_file_by_id(file_id: str) -> Optional[str]:
    prefix = f"{file_id}_"
    logger.debug(f"🔍 Finding file by ID: {file_id}")
    logger.debug(f"   Looking for prefix: {prefix}")
    logger.debug(f"   Storage directory: {settings.storage_dir}")
    
    # Direct approach - check storage directory
    try:
        files = os.listdir(settings.storage_dir)
        logger.debug(f"   Files in storage: {files}")
        
        for filename in files:
            if filename.startswith(prefix) and filename.endswith((".xlsx", ".xls")):
                full_path = os.path.join(settings.storage_dir, filename)
                logger.debug(f"   Found matching file: {filename}")
                logger.debug(f"   Full path: {full_path}")
                if os.path.exists(full_path):
                    logger.debug(f"   ✅ File exists, returning path")
                    return full_path
                else:
                    logger.warning(f"   ❌ File in list but doesn't exist: {full_path}")
    except Exception as e:
        logger.error(f"   Error listing storage directory: {e}")
    
    # Fallback to original method
    logger.debug("   Using fallback method...")
    for path in list_storage_files():
        if os.path.basename(path).startswith(prefix):
            logger.debug(f"   Fallback found: {path}")
            return path
    
    logger.debug(f"   ❌ File not found: {file_id}")
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
    logger.debug(f"🗑️  Attempting to delete file: {file_id}")
    
    file_path = find_file_by_id(file_id)
    logger.debug(f"   Found file path: {file_path}")
    
    if file_path and os.path.exists(file_path):
        try:
            # Get file info before deletion for logging
            file_size = os.path.getsize(file_path)
            logger.debug(f"   File size: {file_size} bytes")
            logger.debug(f"   Deleting file: {file_path}")
            
            os.remove(file_path)
            
            # Verify deletion
            if not os.path.exists(file_path):
                logger.debug(f"   ✅ File successfully deleted")
                return True
            else:
                logger.warning(f"   ❌ File still exists after os.remove()")
                return False
                
        except Exception as e:
            logger.error(f"   ❌ Error deleting file: {e}")
            return False
    else:
        if not file_path:
            logger.debug(f"   ❌ File path not found for ID: {file_id}")
        else:
            logger.debug(f"   ❌ File does not exist: {file_path}")
        return False


