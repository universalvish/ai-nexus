"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, chat, agents, analytics, billing

api_router = APIRouter(prefix="/v1")

# Include all endpoint routers
api_router.include_router(auth.router)
api_router.include_router(chat.router)
api_router.include_router(agents.router)
api_router.include_router(analytics.router)
api_router.include_router(billing.router)