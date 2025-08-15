import os
import uuid
import logging
from typing import List

from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from app.core.config import settings
from app.services.storage import find_file_by_id
from app.services.rag_service import get_rag_service

logger = logging.getLogger("app.api.routes.rag")

router = APIRouter(tags=["rag"])


class RAGUploadResponse(BaseModel):
    fileId: str
    filename: str
    message: str


class RAGQueryRequest(BaseModel):
    fileId: str
    question: str


class RAGQueryResponse(BaseModel):
    answer: str


@router.post("/rag/upload", response_model=RAGUploadResponse)
async def upload_document(file: UploadFile = File(...)) -> RAGUploadResponse:
    """Upload a document (txt, docx, pdf) for RAG processing"""
    filename = file.filename or "uploaded.txt"
    logger.info("="*60)
    logger.info(f"📄 RAG UPLOAD REQUEST")
    logger.info(f"   Original filename: {filename}")
    
    # Check file extension
    if not filename.lower().endswith((".txt", ".docx", ".pdf")):
        logger.error(f"   ❌ Invalid file extension: {filename}")
        raise HTTPException(
            status_code=400, 
            detail="Only .txt, .docx, or .pdf files are supported for RAG"
        )

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
            f.flush()
            os.fsync(f.fileno())
            
        logger.info(f"   ✅ File written to disk")
    except Exception as e:
        logger.error(f"   ❌ Error writing file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {e}")

    # Verify file exists
    if not os.path.exists(saved_path):
        logger.error(f"   ❌ File verification failed")
        raise HTTPException(status_code=500, detail="File save verification failed")
    
    actual_size = os.path.getsize(saved_path)
    logger.info(f"   ✅ File verification passed, size: {actual_size} bytes")

    # Process document with RAG service
    try:
        load_dotenv()
        google_api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise HTTPException(
                status_code=500, 
                detail="GOOGLE_API_KEY is not configured"
            )

        logger.info(f"   🔄 Processing document for RAG...")
        rag_service = get_rag_service(google_api_key)
        rag_service.process_document(saved_path, file_id)
        logger.info(f"   ✅ Document processed and indexed")
        
    except Exception as e:
        logger.error(f"   ❌ Error processing document: {e}")
        # Cleanup file on processing error
        try:
            os.remove(saved_path)
            logger.info(f"   🗑️ Cleaned up file after processing error")
        except Exception as cleanup_e:
            logger.error(f"   ❌ Error cleaning up file: {cleanup_e}")
        raise HTTPException(status_code=400, detail=f"Failed to process document: {e}")

    logger.info(f"   🎉 RAG upload completed successfully")
    logger.info("="*60)
    
    return RAGUploadResponse(
        fileId=file_id,
        filename=filename,
        message="Document uploaded and processed successfully"
    )


@router.post("/rag/query", response_model=RAGQueryResponse)
async def query_document(req: RAGQueryRequest):
    """Query a processed document using RAG"""
    import time
    
    logger.info(f"🔍 RAG QUERY REQUEST")
    logger.info(f"   File ID: {req.fileId}")
    logger.info(f"   Question: {req.question}")
    
    # Find the file
    file_path = find_file_by_id(req.fileId)
    if not file_path:
        logger.error(f"   ❌ File not found: {req.fileId}")
        raise HTTPException(status_code=404, detail="File not found")
    
    # Check if it's a RAG-supported file
    if not file_path.lower().endswith((".txt", ".docx", ".pdf")):
        logger.error(f"   ❌ File type not supported for RAG: {file_path}")
        raise HTTPException(
            status_code=400, 
            detail="File type not supported for RAG. Use .txt, .docx, or .pdf files."
        )
    
    # Get RAG service and query
    try:
        load_dotenv()
        google_api_key = settings.google_api_key or os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise HTTPException(
                status_code=500, 
                detail="GOOGLE_API_KEY is not configured"
            )
        
        rag_service = get_rag_service(google_api_key)
        
        # Retry logic for quota exceeded errors
        max_retries = 3
        for attempt in range(max_retries):
            try:
                logger.info(f"   🤖 Querying document (attempt {attempt + 1})...")
                
                # Run RAG query in thread pool to avoid event loop issues
                import asyncio
                import concurrent.futures
                import functools
                
                def _sync_query():
                    return rag_service.query_document(req.fileId, req.question)
                
                # Run in thread pool executor
                loop = asyncio.get_event_loop()
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    answer = await loop.run_in_executor(executor, _sync_query)
                
                logger.info(f"   ✅ Query completed successfully")
                return RAGQueryResponse(answer=answer)
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Check if it's a quota/rate limit error
                if "quota" in error_msg or "429" in error_msg or "resourceexhausted" in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = 10 * (attempt + 1)  # 10s, 20s, 30s
                        logger.warning(f"   ⏳ Quota exceeded, retrying in {wait_time}s")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"   ❌ Quota exceeded after {max_retries} attempts")
                        raise HTTPException(
                            status_code=429, 
                            detail="Google API quota exceeded. Please wait and try again."
                        )
                else:
                    # Other errors, don't retry
                    logger.error(f"   ❌ Query failed: {e}")
                    raise HTTPException(status_code=500, detail=f"Query failed: {e}")
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"   ❌ Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")


@router.get("/rag/files")
def list_rag_files():
    """List all uploaded RAG files"""
    # This would need to be implemented if we want to track RAG files separately
    # For now, we can use the existing files endpoint and filter by file extension
    raise HTTPException(status_code=501, detail="Not implemented yet")


@router.delete("/rag/file/{file_id}")
def delete_rag_file(file_id: str):
    """Delete a RAG file and its vector data"""
    import shutil
    
    logger.info(f"🗑️ RAG DELETE REQUEST: {file_id}")
    
    # Find and delete the file
    file_path = find_file_by_id(file_id)
    if not file_path:
        logger.error(f"   ❌ File not found: {file_id}")
        raise HTTPException(status_code=404, detail="File not found")
    
    try:
        # Delete the file if it exists
        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"   ✅ File deleted: {file_path}")
        else:
            logger.info(f"   ℹ️  File already deleted: {file_path}")
        
        # Delete vector data directory
        vector_data_dir = os.path.join(settings.storage_dir, "rag_data", file_id)
        if os.path.exists(vector_data_dir):
            shutil.rmtree(vector_data_dir)
            logger.info(f"   ✅ Vector data deleted: {vector_data_dir}")
        else:
            logger.info(f"   ℹ️  Vector data already deleted: {vector_data_dir}")
        
        logger.info(f"   🎉 RAG file deletion completed")
        return {"message": "File and vector data deleted successfully"}
        
    except PermissionError as e:
        logger.error(f"   ❌ Permission denied deleting file: {e}")
        raise HTTPException(status_code=500, detail=f"File may be in use. Please try again later.")
    except Exception as e:
        logger.error(f"   ❌ Error deleting file: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {e}")
