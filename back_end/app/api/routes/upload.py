import os
import uuid
import logging
from typing import List

import pandas as pd
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.core.config import settings

logger = logging.getLogger("app.api.routes.upload")

router = APIRouter(tags=["upload"])


@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)) -> dict:
    filename = file.filename or "uploaded.xlsx"
    logger.info("="*60)
    logger.info(f"📤 UPLOAD FILE REQUEST")
    logger.info(f"   Original filename: {filename}")
    
    if not filename.lower().endswith((".xlsx", ".xls", ".csv")):
        logger.error(f"   ❌ Invalid file extension: {filename}")
        raise HTTPException(status_code=400, detail="Only .xlsx, .xls, or .csv files are supported")

    file_id = str(uuid.uuid4())
    saved_path = os.path.join(settings.storage_dir, f"{file_id}_{filename}")
    logger.info(f"   Generated file ID: {file_id}")
    logger.info(f"   Save path: {saved_path}")

    # Save file to disk
    try:
        with open(saved_path, "wb") as f:
            content = await file.read()
            content_size = len(content)
            logger.info(f"   File size: {content_size} bytes")
            
            f.write(content)
            f.flush()  # Ensure data is written to disk
            os.fsync(f.fileno())  # Force OS to write to storage
            
        logger.info(f"   ✅ File written to disk")
    except Exception as e:
        logger.error(f"   ❌ Error writing file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Verify file exists and is accessible
    if not os.path.exists(saved_path):
        logger.error(f"   ❌ File verification failed - file does not exist")
        raise HTTPException(status_code=500, detail="File save verification failed. Please try again.")
    
    actual_size = os.path.getsize(saved_path)
    logger.info(f"   ✅ File verification passed, size: {actual_size} bytes")
    
    # Read sheet names (for Excel) or validate CSV
    try:
        if filename.lower().endswith(".csv"):
            logger.info(f"   📊 Validating CSV file...")
            # For CSV, just validate it can be read and return a single "sheet"
            pd.read_csv(saved_path, nrows=1)  # Just read first row to validate
            sheet_names: List[str] = ["Sheet1"]  # CSV files have one "sheet"
            logger.info(f"   ✅ CSV file validated successfully")
        else:
            logger.info(f"   📊 Reading Excel sheets...")
            with pd.ExcelFile(saved_path) as xls:
                sheet_names: List[str] = xls.sheet_names
                logger.info(f"   Found {len(sheet_names)} sheets: {sheet_names}")
            logger.info(f"   ✅ Excel file processed successfully")
    except Exception as e:
        logger.error(f"   ❌ Error reading file: {e}")
        # Cleanup invalid file
        try:
            os.remove(saved_path)
            logger.info(f"   🗑️ Cleaned up invalid file")
        except Exception as cleanup_e:
            logger.error(f"   ❌ Error cleaning up file: {cleanup_e}")
        raise HTTPException(status_code=400, detail=f"Failed to read file: {e}")

    logger.info(f"   🎉 Upload completed successfully")
    logger.info("="*60)
    return {"fileId": file_id, "filename": filename, "sheetNames": sheet_names}


