"""Audit logging middleware."""

import json
import time
from typing import Callable
from datetime import datetime

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.enums import AuditAction


class AuditLogMiddleware(BaseHTTPMiddleware):
    """Log all API requests for audit purposes."""

    # Endpoints to exclude from logging
    EXCLUDED_PATHS = {"/", "/health", "/metrics", "/favicon.ico"}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        start_time = time.time()
        
        # Process request
        response = await call_next(request)
        
        # Calculate request duration
        duration = time.time() - start_time

        # Extract request info
        user_id = self._get_user_id(request)
        ip_address = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "")

        # Build audit entry (in production, save to database)
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "user_id": user_id,
            "ip_address": ip_address,
            "user_agent": user_agent[:500] if user_agent else None,
            "duration_ms": round(duration * 1000, 2),
        }

        # Log the audit entry (in production, save to database)
        self._log_audit(audit_entry)

        return response

    def _get_user_id(self, request: Request) -> int | None:
        """Extract user ID from request."""
        # Try to get from JWT token
        auth_header = request.headers.get("authorization", "")
        if auth_header.startswith("Bearer "):
            token = auth_header[7:]
            # In production, decode and extract user ID
            # For now, return None
            pass
        return None

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP address, considering proxies."""
        # Check X-Forwarded-For header first
        forwarded = request.headers.get("x-forwarded-for")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # Check X-Real-IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip
        
        # Fall back to direct client
        if request.client:
            return request.client.host
        return "unknown"

    def _log_audit(self, entry: dict) -> None:
        """Log audit entry. In production, save to database."""
        # In production, save to audit_logs table
        # For now, just print to logs
        import logging
        logger = logging.getLogger("audit")
        logger.info(json.dumps(entry))


def setup_audit_logging(app):
    """Add audit logging middleware to app."""
    app.add_middleware(AuditLogMiddleware)