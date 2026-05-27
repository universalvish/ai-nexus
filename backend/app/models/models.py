"""Database models for the AI Nexus platform."""

from datetime import datetime
from typing import Optional, List
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Text, 
    ForeignKey, Enum, JSON, Float, Index
)
from sqlalchemy.orm import relationship

from app.db.database import Base
from app.core.enums import (
    UserRole, SubscriptionPlan, SubscriptionStatus,
    AgentStatus, AgentType, MessageRole, AlertSeverity
)


class User(Base):
    """User model for authentication and authorization."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    name = Column(String(255), nullable=False)
    avatar_url = Column(String(500), nullable=True)
    role = Column(Enum(UserRole), default=UserRole.USER)
    
    # Subscription
    subscription_plan = Column(Enum(SubscriptionPlan), default=SubscriptionPlan.FREE)
    subscription_status = Column(Enum(SubscriptionStatus), nullable=True)
    subscription_id = Column(String(255), nullable=True)  # Stripe subscription ID
    
    # Trial
    trial_ends_at = Column(DateTime, nullable=True)
    
    # Security
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    two_factor_enabled = Column(Boolean, default=False)
    two_factor_secret = Column(String(255), nullable=True)
    
    # Tracking
    last_login_at = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)
    failed_login_count = Column(Integer, default=0)
    
    # Metadata
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    agents = relationship("Agent", back_populates="user", cascade="all, delete-orphan")
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")


class Conversation(Base):
    """Chat conversation model."""
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    """Chat message model."""
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    content = Column(Text, nullable=False)
    tokens_used = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    conversation = relationship("Conversation", back_populates="messages")
    __table_args__ = (
        Index("idx_messages_conversation_created", "conversation_id", "created_at"),
    )


class Agent(Base):
    """AI Agent model."""
    __tablename__ = "agents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    agent_type = Column(Enum(AgentType), nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.IDLE)
    configuration = Column(JSON, nullable=True)
    system_prompt = Column(Text, nullable=True)
    tools = Column(JSON, nullable=True)
    memory_enabled = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    tasks_completed = Column(Integer, default=0)
    last_active_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="agents")
    executions = relationship("AgentExecution", back_populates="agent", cascade="all, delete-orphan")


class AgentExecution(Base):
    """AI Agent execution log."""
    __tablename__ = "agent_executions"

    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    action = Column(String(255), nullable=False)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    status = Column(String(50), nullable=False)  # success, failed, pending
    error_message = Column(Text, nullable=True)
    execution_time_ms = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    agent = relationship("Agent", back_populates="executions")
    __table_args__ = (
        Index("idx_agent_executions_agent_created", "agent_id", "created_at"),
    )


class Automation(Base):
    """Automation workflow model."""
    __tablename__ = "automations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    trigger_type = Column(String(50), nullable=False)  # cron, webhook, event
    trigger_config = Column(JSON, nullable=False)
    workflow_definition = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime, nullable=True)
    next_run_at = Column(DateTime, nullable=True)
    runs_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AutomationRun(Base):
    """Automation run log."""
    __tablename__ = "automation_runs"

    id = Column(Integer, primary_key=True, index=True)
    automation_id = Column(Integer, ForeignKey("automations.id"), nullable=False)
    status = Column(String(50), nullable=False)  # pending, running, completed, failed
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    """Subscription model for billing."""
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan = Column(Enum(SubscriptionPlan), nullable=False)
    status = Column(Enum(SubscriptionStatus), nullable=False)
    stripe_subscription_id = Column(String(255), nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    current_period_start = Column(DateTime, nullable=True)
    current_period_end = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="subscriptions")


class Invoice(Base):
    """Invoice model for billing."""
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=True)
    stripe_invoice_id = Column(String(255), nullable=True)
    amount = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    status = Column(String(50), nullable=False)  # paid, open, void
    invoice_date = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class APIKey(Base):
    """API Key model for programmatic access."""
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    key_hash = Column(String(255), nullable=False)
    prefix = Column(String(10), nullable=False)
    permissions = Column(JSON, nullable=True)
    rate_limit = Column(Integer, default=1000)  # requests per day
    last_used_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="api_keys")


class AuditLog(Base):
    """Audit log for tracking user actions."""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(100), nullable=False)
    resource_id = Column(String(255), nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    request_data = Column(JSON, nullable=True)
    response_status = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="audit_logs")
    __table_args__ = (
        Index("idx_audit_logs_user_created", "user_id", "created_at"),
        Index("idx_audit_logs_action_created", "action", "created_at"),
    )


class SecurityAlert(Base):
    """Security alert model."""
    __tablename__ = "security_alerts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    severity = Column(Enum(AlertSeverity), nullable=False)
    alert_type = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    ip_address = Column(String(45), nullable=True)
    metadata_json = Column(JSON, nullable=True)
    is_resolved = Column(Boolean, default=False)
    resolved_at = Column(DateTime, nullable=True)
    resolved_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Notification(Base):
    """Notification model for user alerts."""
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    notification_type = Column(String(50), nullable=False)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime, nullable=True)
    metadata_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="notifications")
    __table_args__ = (
        Index("idx_notifications_user_created", "user_id", "created_at"),
    )