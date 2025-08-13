import logging
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
import time

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.api.routes.upload import router as upload_router
from app.api.routes.analyze import router as analyze_router
from app.api.routes.session import router as session_router
from app.api.routes.files import router as files_router

# Setup logging first
setup_logging()
logger = logging.getLogger(__name__)


async def log_requests(request: Request, call_next):
    """Log all HTTP requests and responses"""
    start_time = time.time()
    
    # Log request
    logger.info(f"🔄 {request.method} {request.url}")
    logger.info(f"   Headers: {dict(request.headers)}")
    if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
        logger.info(f"   Query params: {dict(request.query_params)}")
    
    # Process request
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"✅ {response.status_code} | {process_time:.3f}s | {request.method} {request.url}")
    
    return response


def create_app() -> FastAPI:
    app = FastAPI(title="Excel Analysis API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add request logging middleware
    app.middleware("http")(log_requests)

    app.include_router(upload_router, prefix="/api")
    app.include_router(analyze_router, prefix="/api")
    app.include_router(session_router, prefix="/api")
    app.include_router(files_router, prefix="/api")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()


