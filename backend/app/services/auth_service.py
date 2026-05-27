"""Authentication service."""

from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import User
from app.core.security import (
    verify_password, get_password_hash, 
    create_access_token, create_refresh_token, decode_token
)
from app.core.enums import UserRole, SubscriptionPlan


class AuthService:
    """Authentication service for user management."""

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Get user by email."""
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Get user by ID."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_user(
        db: AsyncSession, 
        email: str, 
        password: str, 
        name: str
    ) -> User:
        """Create a new user."""
        user = User(
            email=email,
            hashed_password=get_password_hash(password),
            name=name,
            role=UserRole.USER,
            subscription_plan=SubscriptionPlan.FREE,
        )
        db.add(user)
        await db.flush()
        return user

    @staticmethod
    async def authenticate_user(
        db: AsyncSession, 
        email: str, 
        password: str
    ) -> Optional[User]:
        """Authenticate user with email and password."""
        user = await AuthService.get_user_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            return None
        return user

    @staticmethod
    async def create_tokens(user: User) -> dict:
        """Create access and refresh tokens for user."""
        token_data = {"sub": str(user.id), "email": user.email}
        
        access_token = create_access_token(token_data)
        refresh_token = create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": 1800  # 30 minutes
        }

    @staticmethod
    async def refresh_access_token(refresh_token: str) -> Optional[dict]:
        """Refresh access token using refresh token."""
        payload = decode_token(refresh_token)
        if not payload:
            return None
        
        if payload.get("type") != "refresh":
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        return {"user_id": int(user_id)}

    @staticmethod
    async def update_last_login(db: AsyncSession, user: User) -> None:
        """Update user's last login timestamp."""
        user.last_login_at = datetime.utcnow()
        user.login_count += 1
        user.failed_login_count = 0
        await db.flush()

    @staticmethod
    async def record_failed_login(db: AsyncSession, user: User) -> None:
        """Record a failed login attempt."""
        user.failed_login_count += 1
        
        # Lock account after 5 failed attempts
        if user.failed_login_count >= 5:
            user.is_active = False
        
        await db.flush()

    @staticmethod
    async def update_password(db: AsyncSession, user: User, new_password: str) -> None:
        """Update user's password."""
        user.hashed_password = get_password_hash(new_password)
        await db.flush()

    @staticmethod
    async def verify_user(db: AsyncSession, user: User) -> None:
        """Mark user as verified."""
        user.is_verified = True
        await db.flush()