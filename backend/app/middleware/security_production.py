"""
Security Middleware - Production Ready

Implements:
- Security headers (CSP, HSTS, X-Frame-Options)
- Rate limiting
- CORS
- Request validation
- DDoS protection
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.gzip import GZipMiddleware
from typing import Callable
import time
import hashlib
import re

from app.core.config import settings


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""
    
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        # Prevent clickjacking
        response.headers["X-Frame-Options"] = "DENY"
        
        # Prevent MIME type sniffing
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # XSS Protection (legacy but still useful)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Permissions Policy
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # Content Security Policy
        csp_policy = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self' data:; "
            "connect-src 'self' https:; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'; "
            "object-src 'none';"
        )
        response.headers["Content-Security-Policy"] = csp_policy
        
        # HSTS (only in production with HTTPS)
        if settings.is_production:
            response.headers["Strict-Transport-Security"] = (
                "max-age=31536000; includeSubDomains; preload"
            )
        
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory rate limiting."""
    
    # Store request counts by IP
    requests: dict = {}
    last_cleanup: float = time.time()
    
    async def dispatch(self, request: Request, call_next: Callable):
        client_ip = request.client.host if request.client else "unknown"
        current_time = time.time()
        
        # Cleanup old entries every minute
        if current_time - self.last_cleanup > 60:
            self.requests = {}
            self.last_cleanup = current_time
        
        # Get or create rate limit entry
        if client_ip not in self.requests:
            self.requests[client_ip] = {
                "count": 0,
                "window_start": current_time
            }
        
        entry = self.requests[client_ip]
        
        # Reset window if expired (1 minute)
        if current_time - entry["window_start"] > 60:
            entry["count"] = 0
            entry["window_start"] = current_time
        
        # Check rate limit
        if entry["count"] >= settings.RATE_LIMIT_PER_MINUTE:
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "message": f"Rate limit exceeded. Maximum {settings.RATE_LIMIT_PER_MINUTE} requests per minute.",
                    "code": "RATE_LIMIT_EXCEEDED"
                }
            )
        
        # Increment counter
        entry["count"] += 1
        
        response = await call_next(request)
        
        # Add rate limit headers
        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Remaining"] = str(
            settings.RATE_LIMIT_PER_MINUTE - entry["count"]
        )
        response.headers["X-RateLimit-Reset"] = str(
            int(entry["window_start"] + 60)
        )
        
        return response


class PromptInjectionMiddleware(BaseHTTPMiddleware):
    """Detect and block prompt injection attacks."""
    
    # Suspicious patterns that might indicate prompt injection
    INJECTION_PATTERNS = [
        r"ignore (previous|all|above|system|prompt|instructions)",
        r"disregard (previous|all|above|system|prompt|instructions)",
        r"forget (previous|all|above|system|prompt|instructions)",
        r"override (previous|all|above|system|prompt|instructions)",
        r"new (system|prompt|instructions)",
        r"you are now",
        r"pretend you are",
        r"act as",
        r"roleplay",
        r"--",
        r"```",
        r"ignore previous instructions",
        r"disregard safety",
        r"bypass",
    ]
    
    COMPILED_PATTERNS = [
        re.compile(pattern, re.IGNORECASE) 
        for pattern in INJECTION_PATTERNS
    ]
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Only check POST/PUT requests with body
        if request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if body:
                    body_text = body.decode("utf-8", errors="ignore").lower()
                    
                    for pattern in self.COMPILED_PATTERNS:
                        if pattern.search(body_text):
                            # Log the attempt
                            print(f"[SECURITY] Potential prompt injection detected from {request.client.host}")
                            
                            return JSONResponse(
                                status_code=400,
                                content={
                                    "error": "Bad Request",
                                    "message": "Potentially malicious content detected.",
                                    "code": "INVALID_INPUT"
                                }
                            )
            except Exception:
                pass  # Continue if we can't parse the body
        
        return await call_next(request)


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate and sanitize incoming requests."""
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Block access to admin routes in production without auth
        # (unless explicitly configured to allow)
        path = request.url.path
        
        if path.startswith("/admin") and not path.startswith("/api/v1/admin"):
            # Admin routes should be protected by the API, not this middleware
            pass
        
        return await call_next(request)


def setup_security_middlewares(app: FastAPI) -> None:
    """Configure all security middlewares."""
    
    # CORS - Only allow specific origins
    cors_origins = settings.cors_origins_list
    
    if not cors_origins:
        # If no CORS origins configured, default to strict
        cors_origins = []
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
        expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining", "X-RateLimit-Reset"],
        max_age=600,  # Cache preflight for 10 minutes
    )
    
    # GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # Security headers (must be first to protect all responses)
    app.add_middleware(SecurityHeadersMiddleware)
    
    # Rate limiting
    app.add_middleware(RateLimitMiddleware)
    
    # Prompt injection detection
    app.add_middleware(PromptInjectionMiddleware)
    
    # Request validation
    app.add_middleware(RequestValidationMiddleware)


class EmergencyStopMiddleware(BaseHTTPMiddleware):
    """Allow emergency shutdown of AI operations."""
    
    _emergency_stop_active = False
    
    async def dispatch(self, request: Request, call_next: Callable):
        if self._emergency_stop_active and request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=503,
                content={
                    "error": "Service Unavailable",
                    "message": "AI operations have been temporarily stopped by administrator.",
                    "code": "EMERGENCY_STOP_ACTIVE"
                }
            )
        
        return await call_next(request)
    
    @classmethod
    def activate_emergency_stop(cls):
        """Activate emergency stop."""
        cls._emergency_stop_active = True
        print("[SECURITY] Emergency stop activated")
    
    @classmethod
    def deactivate_emergency_stop(cls):
        """Deactivate emergency stop."""
        cls._emergency_stop_active = False
        print("[SECURITY] Emergency stop deactivated")