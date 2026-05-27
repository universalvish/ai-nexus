from enum import Enum


class UserRole(str, Enum):
    """User role enumeration."""
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MODERATOR = "moderator"
    PREMIUM_USER = "premium_user"
    USER = "user"


class SubscriptionPlan(str, Enum):
    """Subscription plan enumeration."""
    FREE = "free"
    PRO = "pro"
    BUSINESS = "business"
    ENTERPRISE = "enterprise"


class SubscriptionStatus(str, Enum):
    """Subscription status enumeration."""
    TRIALING = "trialing"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    INCOMPLETE = "incomplete"


class AgentStatus(str, Enum):
    """AI agent status enumeration."""
    ACTIVE = "active"
    IDLE = "idle"
    ERROR = "error"
    DISABLED = "disabled"


class AgentType(str, Enum):
    """AI agent type enumeration."""
    CUSTOMER_SUPPORT = "customer_support"
    REPORT_GENERATOR = "report_generator"
    DATA_ANALYST = "data_analyst"
    CONTENT_GENERATOR = "content_generator"
    WORKFLOW_AUTOMATOR = "workflow_automator"
    TICKET_MANAGER = "ticket_manager"
    EMAIL_ASSISTANT = "email_assistant"


class MessageRole(str, Enum):
    """Chat message role enumeration."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class AuditAction(str, Enum):
    """Audit action enumeration."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    FAILED_LOGIN = "failed_login"
    PASSWORD_CHANGE = "password_change"
    PERMISSION_CHANGE = "permission_change"
    API_ACCESS = "api_access"
    AI_QUERY = "ai_query"
    AGENT_EXECUTION = "agent_execution"


class AlertSeverity(str, Enum):
    """Security alert severity enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"