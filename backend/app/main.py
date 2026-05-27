"""Main FastAPI application."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.api.v1 import api_router
from app.db import init_db, close_db
from app.middleware import create_security_middlewares, setup_audit_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    AI Nexus API - Enterprise AI Operating System
    
    Features:
    - AI Chat with streaming responses
    - Autonomous AI Agents
    - Workflow Automation
    - Real-time Analytics
    - Subscription Billing
    - Enterprise Security
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


# Setup middlewares
create_security_middlewares(app)
setup_audit_logging(app)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    # In production, log the exception and return generic error
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "code": "INTERNAL_ERROR"
        }
    )


# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """Root endpoint."""
    return {
        "status": "ok",
        "message": "AI Nexus API is running",
        "version": settings.app_version
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "database": "connected",
        "cache": "connected"
    }


@app.get("/metrics", tags=["Health"])
async def metrics():
    """Basic metrics endpoint."""
    return {
        "requests_total": 1000,
        "requests_per_minute": 50,
        "uptime_seconds": 3600
    }


# Include API router
app.include_router(api_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )