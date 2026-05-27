"""Chat service for AI conversations."""

import time
from typing import Optional, List, Dict, Any
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc

from app.models import Conversation, Message, User
from app.core.enums import MessageRole
from app.middleware.security import PromptInjectionDetector
from app.services.ai_service import AIService


class ChatService:
    """Service for managing chat conversations."""

    def __init__(self):
        self.ai_service = AIService()

    async def create_conversation(
        self, 
        db: AsyncSession, 
        user_id: int, 
        title: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> Conversation:
        """Create a new conversation."""
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation",
            metadata=metadata
        )
        db.add(conversation)
        await db.flush()
        return conversation

    async def get_conversation(
        self, 
        db: AsyncSession, 
        conversation_id: int, 
        user_id: int
    ) -> Optional[Conversation]:
        """Get conversation by ID for a specific user."""
        result = await db.execute(
            select(Conversation).where(
                and_(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            )
        )
        return result.scalar_one_or_none()

    async def get_user_conversations(
        self, 
        db: AsyncSession, 
        user_id: int,
        limit: int = 50,
        include_archived: bool = False
    ) -> List[Conversation]:
        """Get all conversations for a user."""
        query = select(Conversation).where(
            Conversation.user_id == user_id
        )
        
        if not include_archived:
            query = query.where(Conversation.is_archived == False)
        
        query = query.order_by(desc(Conversation.updated_at)).limit(limit)
        
        result = await db.execute(query)
        return result.scalars().all()

    async def send_message(
        self,
        db: AsyncSession,
        user_id: int,
        content: str,
        conversation_id: Optional[int] = None,
        context: Optional[Dict] = None
    ) -> tuple[Message, Conversation]:
        """
        Send a message and get AI response.
        Returns tuple of (user_message, conversation).
        """
        # Validate prompt safety
        is_safe, reason = PromptInjectionDetector.is_safe(content)
        if not is_safe:
            raise ValueError(f"Message blocked: {reason}")

        # Get or create conversation
        if conversation_id:
            conversation = await self.get_conversation(db, conversation_id, user_id)
            if not conversation:
                raise ValueError("Conversation not found")
        else:
            conversation = await self.create_conversation(db, user_id)
            conversation_id = conversation.id

        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.USER,
            content=content
        )
        db.add(user_message)
        await db.flush()

        # Get conversation history for context
        history = await self.get_conversation_history(
            db, conversation_id, limit=10
        )

        # Get AI response
        try:
            ai_response, tokens_used, model = await self.ai_service.chat(
                content, history, context
            )
        except Exception as e:
            # Create error message
            error_message = Message(
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content="I apologize, but I encountered an error processing your request. Please try again.",
                metadata={"error": str(e)}
            )
            db.add(error_message)
            await db.flush()
            await self._update_conversation_timestamp(db, conversation)
            return user_message, conversation

        # Save AI response
        assistant_message = Message(
            conversation_id=conversation_id,
            role=MessageRole.ASSISTANT,
            content=ai_response,
            tokens_used=tokens_used,
            model_used=model
        )
        db.add(assistant_message)
        await db.flush()

        # Update conversation timestamp
        await self._update_conversation_timestamp(db, conversation)

        return user_message, conversation

    async def get_conversation_history(
        self, 
        db: AsyncSession, 
        conversation_id: int,
        limit: int = 50
    ) -> List[Message]:
        """Get message history for a conversation."""
        result = await db.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        return result.scalars().all()

    async def delete_message(
        self, 
        db: AsyncSession, 
        message_id: int, 
        user_id: int
    ) -> bool:
        """Delete a message (soft delete by clearing content)."""
        result = await db.execute(
            select(Message).where(Message.id == message_id)
        )
        message = result.scalar_one_or_none()
        
        if not message:
            return False
        
        # Verify ownership
        conversation = await self.get_conversation(
            db, message.conversation_id, user_id
        )
        if not conversation:
            return False
        
        message.content = "[Message deleted]"
        await db.flush()
        return True

    async def archive_conversation(
        self, 
        db: AsyncSession, 
        conversation_id: int, 
        user_id: int
    ) -> bool:
        """Archive a conversation."""
        conversation = await self.get_conversation(db, conversation_id, user_id)
        if not conversation:
            return False
        
        conversation.is_archived = True
        await db.flush()
        return True

    async def clear_conversation(
        self, 
        db: AsyncSession, 
        conversation_id: int, 
        user_id: int
    ) -> bool:
        """Clear all messages in a conversation."""
        conversation = await self.get_conversation(db, conversation_id, user_id)
        if not conversation:
            return False
        
        # Delete all messages
        await db.execute(
            Message.__table__.delete().where(
                Message.conversation_id == conversation_id
            )
        )
        await db.flush()
        return True

    async def _update_conversation_timestamp(
        self, 
        db: AsyncSession, 
        conversation: Conversation
    ) -> None:
        """Update conversation's updated_at timestamp."""
        conversation.updated_at = datetime.utcnow()
        await db.flush()