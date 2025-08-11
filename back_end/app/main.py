from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.upload import router as upload_router
from app.api.routes.analyze import router as analyze_router
from app.api.routes.session import router as session_router
from app.api.routes.files import router as files_router


def create_app() -> FastAPI:
    app = FastAPI(title="Excel Analysis API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(upload_router, prefix="/api")
    app.include_router(analyze_router, prefix="/api")
    app.include_router(session_router, prefix="/api")
    app.include_router(files_router, prefix="/api")

    @app.get("/health")
    def health_check():
        return {"status": "ok"}

    return app


app = create_app()


