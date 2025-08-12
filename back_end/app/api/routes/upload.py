import os
import uuid
from typing import List

import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings

router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)) -> dict:
    filename = file.filename or "uploaded.xlsx"
    if not filename.lower().endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Only .xlsx or .xls files are supported")

    file_id = str(uuid.uuid4())
    saved_path = os.path.join(settings.storage_dir, f"{file_id}_{filename}")

    # Save file to disk
    with open(saved_path, "wb") as f:
        content = await file.read()
        f.write(content)
        f.flush()  # Ensure data is written to disk
        os.fsync(f.fileno())  # Force OS to write to storage

    # Verify file exists and is accessible
    if not os.path.exists(saved_path):
        raise HTTPException(status_code=500, detail="File save verification failed")
    
    # Read sheet names
    try:
        xls = pd.ExcelFile(saved_path)
        sheet_names: List[str] = xls.sheet_names
        xls.close()  # Explicitly close to release file handle
    except Exception as e:
        # Cleanup invalid file
        try:
            os.remove(saved_path)
        except Exception:
            pass
        raise HTTPException(status_code=400, detail=f"Failed to read Excel file: {e}")

    return {"fileId": file_id, "filename": filename, "sheetNames": sheet_names}


