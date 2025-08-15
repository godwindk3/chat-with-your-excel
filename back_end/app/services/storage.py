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
            # Support both Excel and RAG files
            if filename.startswith(prefix) and filename.endswith((".xlsx", ".xls", ".txt", ".docx", ".pdf")):
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
    """List only Excel files for pandas agent"""
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


def list_all_files() -> List[Dict[str, Any]]:
    """List all uploaded files (Excel, txt, docx, pdf)"""
    files = []
    try:
        for name in os.listdir(settings.storage_dir):
            # Skip session files and files without proper naming convention
            if name.startswith("session_") or not ("_" in name):
                continue
            
            # Check if it's a supported file type
            if not name.endswith((".xlsx", ".xls", ".txt", ".docx", ".pdf")):
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


def delete_file_by_id(file_id: str) -> tuple[bool, str]:
    """
    Delete file by ID.
    Returns: (success: bool, error_message: str)
    """
    logger.debug(f"🗑️  Attempting to delete file: {file_id}")
    
    file_path = find_file_by_id(file_id)
    logger.debug(f"   Found file path: {file_path}")
    
    if not file_path:
        logger.debug(f"   ❌ File path not found for ID: {file_id}")
        return False, "File not found"
    
    if not os.path.exists(file_path):
        logger.debug(f"   ❌ File does not exist: {file_path}")
        return False, "File not found"
    
    try:
        # Get file info before deletion for logging
        file_size = os.path.getsize(file_path)
        logger.debug(f"   File size: {file_size} bytes")
        logger.debug(f"   Deleting file: {file_path}")
        
        os.remove(file_path)
        
        # Verify deletion
        if not os.path.exists(file_path):
            logger.debug(f"   ✅ File successfully deleted")
            return True, ""
        else:
            logger.warning(f"   ❌ File still exists after os.remove()")
            return False, "File deletion verification failed"
            
    except PermissionError as e:
        logger.warning(f"   🔒 File is locked/in use: {e}")
        return False, "File is currently in use. Please close any applications using this file and try again."
    except OSError as e:
        logger.error(f"   ❌ OS error deleting file: {e}")
        return False, f"Cannot delete file: {e}"
    except Exception as e:
        logger.error(f"   ❌ Unexpected error deleting file: {e}")
        return False, f"Unexpected error: {e}"


