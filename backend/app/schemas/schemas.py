"""Pydantic schemas for API request/response validation."""

from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from app.core.enums import UserRole, SubscriptionPlan, SubscriptionStatus, AgentStatus, AgentType, MessageRole


# ============ Auth Schemas ============

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    name: str = Field(..., min_length=1, max_length=255)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    email: str
    name: str
    avatar_url: Optional[str] = None
    role: UserRole
    subscription_plan: SubscriptionPlan
    is_verified: bool
    is_active: bool
    created_at: datetime


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)


# ============ Chat Schemas ============

class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[int] = None


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    conversation_id: int
    role: MessageRole
    content: str
    tokens_used: Optional[int] = None
    model_used: Optional[str] = None
    created_at: datetime


class ConversationCreate(BaseModel):
    title: Optional[str] = None
    metadata_json: Optional[dict] = None


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    title: Optional[str] = None
    is_archived: bool
    created_at: datetime
    updated_at: datetime
    messages: Optional[List[MessageResponse]] = []


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[int] = None
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    message: str
    conversation_id: int
    tokens_used: Optional[int] = None
    model: str


# ============ Agent Schemas ============

class AgentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    agent_type: AgentType
    configuration: Optional[dict] = None
    system_prompt: Optional[str] = None
    tools: Optional[List[str]] = None
    memory_enabled: bool = True


class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[AgentStatus] = None
    configuration: Optional[dict] = None
    system_prompt: Optional[str] = None
    tools: Optional[List[str]] = None
    memory_enabled: Optional[bool] = None
    is_active: Optional[bool] = None


class AgentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    agent_type: AgentType
    status: AgentStatus
    configuration: Optional[dict] = None
    system_prompt: Optional[str] = None
    tools: Optional[List[str]] = None
    memory_enabled: bool
    is_active: bool
    tasks_completed: int
    last_active_at: Optional[datetime] = None
    created_at: datetime


class AgentExecuteRequest(BaseModel):
    action: str = Field(..., min_length=1, max_length=255)
    params: Optional[dict] = None


class AgentExecutionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    agent_id: int
    action: str
    output_data: Optional[dict] = None
    status: str
    error_message: Optional[str] = None
    execution_time_ms: Optional[int] = None
    created_at: datetime


# ============ Automation Schemas ============

class AutomationCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    trigger_type: str  # cron, webhook, event
    trigger_config: dict
    workflow_definition: dict


class AutomationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    trigger_config: Optional[dict] = None
    workflow_definition: Optional[dict] = None
    is_active: Optional[bool] = None


class AutomationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    name: str
    description: Optional[str] = None
    trigger_type: str
    trigger_config: dict
    workflow_definition: dict
    is_active: bool
    last_run_at: Optional[datetime] = None
    next_run_at: Optional[datetime] = None
    runs_count: int
    success_count: int
    failure_count: int
    created_at: datetime


class AutomationRunResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    automation_id: int
    status: str
    output_data: Optional[dict] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime


# ============ Billing Schemas ============

class PlanResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    currency: str
    interval: str
    features: List[str]
    limits: dict


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    plan: SubscriptionPlan
    status: SubscriptionStatus
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    canceled_at: Optional[datetime] = None
    created_at: datetime


class CheckoutRequest(BaseModel):
    plan_id: str
    success_url: str
    cancel_url: str


class InvoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    amount: float
    currency: str
    status: str
    invoice_date: Optional[datetime] = None
    paid_at: Optional[datetime] = None
    created_at: datetime


# ============ Analytics Schemas ============

class DashboardMetrics(BaseModel):
    total_users: int
    active_agents: int
    total_conversations: int
    api_requests_today: int
    revenue_mtd: float
    active_subscriptions: int


class UsageMetrics(BaseModel):
    date: str
    messages_count: int
    tokens_used: int
    active_users: int
    agents_executed: int


class AnalyticsResponse(BaseModel):
    metrics: DashboardMetrics
    usage: List[UsageMetrics]


# ============ Common Schemas ============

class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)
    sort_by: Optional[str] = None
    sort_order: Optional[str] = Field(default="desc", pattern="^(asc|desc)$")


class PaginatedResponse(BaseModel):
    items: List[Any]
    total: int
    page: int
    limit: int
    pages: int


class ErrorResponse(BaseModel):
    error: str
    message: str
    code: Optional[str] = None
    details: Optional[dict] = None


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
    data: Optional[dict] = None