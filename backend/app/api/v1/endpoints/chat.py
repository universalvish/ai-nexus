"""Chat API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import (
    MessageResponse, ConversationCreate, ConversationResponse,
    ChatRequest, ChatResponse, SuccessResponse, PaginatedResponse
)
from app.services.chat_service import ChatService
from app.api.deps import get_current_user
from app.models import User

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send a message and get AI response."""
    chat_service = ChatService()
    
    try:
        user_message, conversation = await chat_service.send_message(
            db=db,
            user_id=current_user.id,
            content=request.message,
            conversation_id=request.conversation_id,
            context=request.context
        )
        
        # Get the assistant response
        messages = await chat_service.get_conversation_history(
            db, conversation.id, limit=2
        )
        
        assistant_msg = messages[-1] if messages else None
        
        return ChatResponse(
            message=assistant_msg.content if assistant_msg else "No response",
            conversation_id=conversation.id,
            tokens_used=assistant_msg.tokens_used if assistant_msg else None,
            model=assistant_msg.model_used if assistant_msg else "unknown"
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/conversations", response_model=List[ConversationResponse])
async def list_conversations(
    limit: int = 50,
    include_archived: bool = False,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all conversations for current user."""
    chat_service = ChatService()
    conversations = await chat_service.get_user_conversations(
        db, current_user.id, limit, include_archived
    )
    return [ConversationResponse.model_validate(c) for c in conversations]


@router.post("/conversations", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    request: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new conversation."""
    chat_service = ChatService()
    conversation = await chat_service.create_conversation(
        db, current_user.id, request.title, request.metadata
    )
    return ConversationResponse.model_validate(conversation)


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific conversation with messages."""
    chat_service = ChatService()
    conversation = await chat_service.get_conversation(
        db, conversation_id, current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    # Get messages
    messages = await chat_service.get_conversation_history(db, conversation_id)
    
    response = ConversationResponse.model_validate(conversation)
    response.messages = [MessageResponse.model_validate(m) for m in messages]
    
    return response


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
async def get_conversation_messages(
    conversation_id: int,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get messages for a conversation."""
    chat_service = ChatService()
    
    # Verify ownership
    conversation = await chat_service.get_conversation(
        db, conversation_id, current_user.id
    )
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    messages = await chat_service.get_conversation_history(
        db, conversation_id, limit
    )
    
    return [MessageResponse.model_validate(m) for m in messages]


@router.delete("/conversations/{conversation_id}", response_model=SuccessResponse)
async def archive_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Archive a conversation."""
    chat_service = ChatService()
    success = await chat_service.archive_conversation(
        db, conversation_id, current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return SuccessResponse(message="Conversation archived")


@router.delete("/conversations/{conversation_id}/messages", response_model=SuccessResponse)
async def clear_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Clear all messages in a conversation."""
    chat_service = ChatService()
    success = await chat_service.clear_conversation(
        db, conversation_id, current_user.id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return SuccessResponse(message="Conversation cleared")