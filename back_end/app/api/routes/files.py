from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import pandas as pd

from app.services.storage import list_uploaded_files, delete_file_by_id, find_file_by_id

router = APIRouter(tags=["files"])


class FileInfo(BaseModel):
    fileId: str
    filename: str
    size: int
    uploadedAt: float


class FileInfoWithSheets(BaseModel):
    fileId: str
    filename: str
    sheetNames: List[str]


@router.get("/files", response_model=List[FileInfo])
def list_files():
    files = list_uploaded_files()
    return [
        FileInfo(
            fileId=f["fileId"],
            filename=f["filename"],
            size=f["size"],
            uploadedAt=f["uploadedAt"]
        )
        for f in files
    ]


@router.get("/files/{file_id}/info", response_model=FileInfoWithSheets)
def get_file_info(file_id: str):
    file_path = find_file_by_id(file_id)
    if not file_path:
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Read sheet names from the Excel file
        xls = pd.ExcelFile(file_path)
        sheet_names: List[str] = xls.sheet_names
        
        # Get filename from path
        import os
        filename = os.path.basename(file_path)
        if "_" in filename:
            filename = "_".join(filename.split("_")[1:])  # Remove file_id prefix
            
        return FileInfoWithSheets(
            fileId=file_id,
            filename=filename,
            sheetNames=sheet_names
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to read Excel file: {e}")


@router.delete("/files/{file_id}")
def delete_file(file_id: str):
    import time
    import logging
    import os
    
    logger = logging.getLogger("app.api.routes.files")
    logger.info("="*60)
    logger.info(f"🗑️  DELETE FILE REQUEST")
    logger.info(f"   File ID: {file_id}")
    logger.info(f"   Request time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check storage directory status
    from app.core.config import settings
    logger.info(f"   Storage directory: {settings.storage_dir}")
    logger.info(f"   Storage exists: {os.path.exists(settings.storage_dir)}")
    
    if os.path.exists(settings.storage_dir):
        try:
            files_in_storage = os.listdir(settings.storage_dir)
            logger.info(f"   Files in storage ({len(files_in_storage)}): {files_in_storage}")
        except Exception as e:
            logger.error(f"   Error listing storage: {e}")
    
    # Check if file exists before attempting delete
    from app.services.storage import find_file_by_id
    file_path = find_file_by_id(file_id)
    logger.info(f"   File path found: {file_path}")
    
    if file_path:
        logger.info(f"   File exists on disk: {os.path.exists(file_path)}")
        if os.path.exists(file_path):
            try:
                file_size = os.path.getsize(file_path)
                file_mtime = os.path.getmtime(file_path)
                logger.info(f"   File size: {file_size} bytes")
                logger.info(f"   File modified: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_mtime))}")
            except Exception as e:
                logger.error(f"   Error getting file stats: {e}")
    else:
        logger.warning(f"   ❌ File not found by ID: {file_id}")
        # List all files with the ID pattern to debug
        try:
            all_files = os.listdir(settings.storage_dir)
            matching_files = [f for f in all_files if f.startswith(f"{file_id}_")]
            logger.info(f"   Files matching pattern '{file_id}_*': {matching_files}")
        except Exception as e:
            logger.error(f"   Error checking pattern: {e}")
    
    # Retry logic for race condition with recent uploads
    logger.info("   Starting delete attempts...")
    for attempt in range(3):
        logger.info(f"   🔄 Delete attempt {attempt + 1}/3")
        success = delete_file_by_id(file_id)
        logger.info(f"   ➡️ Delete result: {success}")
        
        if success:
            logger.info(f"   ✅ File deleted successfully on attempt {attempt + 1}")
            logger.info("="*60)
            return {"message": "File deleted successfully"}
        
        # Short delay before retry (only for first 2 attempts)
        if attempt < 2:
            logger.info(f"   ⏳ Waiting 100ms before retry...")
            time.sleep(0.1)  # 100ms delay
    
    logger.error(f"   ❌ Failed to delete file after 3 attempts")
    logger.info("="*60)
    raise HTTPException(status_code=404, detail="File not found")
