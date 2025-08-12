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
    
    # Retry logic for race condition with recent uploads
    for attempt in range(3):
        success = delete_file_by_id(file_id)
        if success:
            return {"message": "File deleted successfully"}
        
        # Short delay before retry (only for first 2 attempts)
        if attempt < 2:
            time.sleep(0.1)  # 100ms delay
    
    raise HTTPException(status_code=404, detail="File not found")
