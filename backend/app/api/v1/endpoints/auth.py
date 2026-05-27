"""Authentication API endpoints."""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import (
    UserCreate, UserLogin, UserResponse, UserUpdate,
    TokenResponse, RefreshTokenRequest, PasswordResetRequest, PasswordResetConfirm,
    SuccessResponse, ErrorResponse
)
from app.services.auth_service import AuthService
from app.api.deps import get_current_user
from app.models import User
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if email already exists
    existing_user = await AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = await AuthService.create_user(
        db, 
        user_data.email, 
        user_data.password, 
        user_data.name
    )
    
    # Create tokens
    tokens = await AuthService.create_tokens(user)
    
    return TokenResponse(**tokens)


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with email and password."""
    # Authenticate user
    user = await AuthService.authenticate_user(
        db, 
        credentials.email, 
        credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Update last login
    await AuthService.update_last_login(db, user)
    
    # Create tokens
    tokens = await AuthService.create_tokens(user)
    
    return TokenResponse(**tokens)


@router.post("/logout", response_model=SuccessResponse)
async def logout(
    current_user: User = Depends(get_current_user)
):
    """Logout current user."""
    # In production, you might want to blacklist the token
    return SuccessResponse(message="Successfully logged out")


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token."""
    result = await AuthService.refresh_access_token(request.refresh_token)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )
    
    user = await AuthService.get_user_by_id(db, result["user_id"])
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    tokens = await AuthService.create_tokens(user)
    return TokenResponse(**tokens)


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    if user_data.name is not None:
        current_user.name = user_data.name
    if user_data.avatar_url is not None:
        current_user.avatar_url = user_data.avatar_url
    
    await db.flush()
    return UserResponse.model_validate(current_user)


@router.post("/password/reset", response_model=SuccessResponse)
async def request_password_reset(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    """Request password reset email."""
    user = await AuthService.get_user_by_email(db, request.email)
    
    # Always return success to prevent email enumeration
    if not user:
        return SuccessResponse(
            message="If the email exists, a reset link has been sent"
        )
    
    # In production, send email with reset link
    # For demo, just return success
    
    return SuccessResponse(
        message="If the email exists, a reset link has been sent"
    )


@router.post("/password/reset/confirm", response_model=SuccessResponse)
async def confirm_password_reset(
    request: PasswordResetConfirm,
    db: AsyncSession = Depends(get_db)
):
    """Reset password using token."""
    from app.core.security import verify_password_reset_token
    
    email = verify_password_reset_token(request.token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    user = await AuthService.get_user_by_email(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User not found"
        )
    
    await AuthService.update_password(db, user, request.new_password)
    
    return SuccessResponse(message="Password successfully reset")