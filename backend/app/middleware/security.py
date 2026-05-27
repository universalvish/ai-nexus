"""Security middleware for rate limiting, CORS, and request validation."""

import time
from typing import Callable, Dict, Optional
from collections import defaultdict
import re

from fastapi import Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware as FastAPICORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings


# Rate limiter instance
limiter = Limiter(key_func=get_remote_address)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Custom rate limiting middleware."""

    def __init__(self, app, requests_per_minute: int = 60, burst: int = 10):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.burst = burst
        self.request_counts: Dict[str, list] = defaultdict(list)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = get_remote_address(request)
        current_time = time.time()

        # Clean old requests (older than 1 minute)
        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip]
            if current_time - timestamp < 60
        ]

        # Check rate limit
        if len(self.request_counts[client_ip]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded. Please try again later."
            )

        # Add current request
        self.request_counts[client_ip].append(current_time)

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = str(self.requests_per_minute)
        response.headers["X-RateLimit-Remaining"] = str(
            self.requests_per_minute - len(self.request_counts[client_ip])
        )
        return response


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Add security headers to all responses."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-DNS-Prefetch-Control"] = "on"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        
        # HSTS (only in production)
        if not settings.debug:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Content Security Policy
        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self' https://api.openai.com https://api.anthropic.com; "
            "frame-ancestors 'none';"
        )
        response.headers["Content-Security-Policy"] = csp
        
        return response


class InputValidationMiddleware(BaseHTTPMiddleware):
    """Validate and sanitize input data."""

    # Blocked patterns for SQL injection prevention
    SQL_INJECTION_PATTERNS = [
        r"(\b(union|select|insert|update|delete|drop|create|alter|exec|execute)\b)",
        r"(--|;|'|\"|\\|\*|\%)",
        r"(0x[0-9a-f]+)",
    ]

    # Blocked patterns for XSS prevention
    XSS_PATTERNS = [
        r"(<script|<\/script>|<iframe|<\/iframe>)",
        r"(javascript:|onerror=|onclick=|onload=)",
        r"(&lt;script|&lt;/script|&lt;iframe)",
    ]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip validation for static files
        if request.url.path.startswith("/static"):
            return await call_next(request)

        # Validate query parameters
        for param, value in request.query_params.items():
            if self._contains_malicious_pattern(value, self.SQL_INJECTION_PATTERNS):
                raise HTTPException(
                    status_code=400,
                    detail="Invalid input detected"
                )

        response = await call_next(request)
        return response

    def _contains_malicious_pattern(self, value: str, patterns: list) -> bool:
        """Check if value contains any malicious patterns."""
        if not isinstance(value, str):
            return False
        for pattern in patterns:
            if re.search(pattern, value, re.IGNORECASE):
                return True
        return False


def setup_cors(app):
    """Configure CORS middleware."""
    app.add_middleware(
        FastAPICORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type", "X-Requested-With"],
        expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining"],
        max_age=3600,
    )


class PromptInjectionDetector:
    """Detect and block prompt injection attempts."""

    INJECTION_PATTERNS = [
        r"ignore (previous|above|all) instructions",
        r"disregard (previous|above|all) instructions",
        r"you are now (?:a |an )?\{[a-z_]+\}",
        r"(?:system prompt|prompt):",
        r"\\n(?:system|assistant|user):",
        r"(?:forget|ignore|skip) (?:your |the )?instructions",
        r"roleplay as (?:a |an )?",
        r"pretend (?:you are|i am)",
        r"\[INST\]|\[/INST\]",
        r"<\|[a-z_]+\|>",
        r"(?:ignore|disregard) (?:this|that)",
    ]

    @classmethod
    def is_safe(cls, prompt: str) -> tuple[bool, Optional[str]]:
        """Check if prompt is safe. Returns (is_safe, reason)."""
        if not isinstance(prompt, str):
            return False, "Invalid prompt type"

        # Check for injection patterns
        for pattern in cls.INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                return False, "Potential prompt injection detected"

        # Check for excessive length (possible attack vector)
        if len(prompt) > 10000:
            return False, "Prompt exceeds maximum length"

        return True, None


def create_security_middlewares(app):
    """Set up all security middlewares."""
    # CORS
    setup_cors(app)
    
    # Custom middlewares
    app.add_middleware(SecurityHeadersMiddleware)
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=settings.rate_limit_per_minute,
        burst=settings.rate_limit_burst
    )
    app.add_middleware(InputValidationMiddleware)