"""Analytics API endpoints."""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.db import get_db
from app.schemas import (
    AnalyticsResponse, DashboardMetrics, UsageMetrics,
    ErrorResponse
)
from app.api.deps import get_current_user, require_admin
from app.models import User, Conversation, Message, Agent, AgentExecution, Subscription

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard_metrics(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard metrics."""
    # Count users
    users_result = await db.execute(select(func.count(User.id)))
    total_users = users_result.scalar() or 0
    
    # Count active agents
    agents_result = await db.execute(
        select(func.count(Agent.id)).where(Agent.status == "active")
    )
    active_agents = agents_result.scalar() or 0
    
    # Count conversations
    conv_result = await db.execute(
        select(func.count(Conversation.id))
    )
    total_conversations = conv_result.scalar() or 0
    
    # Count messages today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    messages_result = await db.execute(
        select(func.count(Message.id))
        .where(Message.created_at >= today_start)
    )
    api_requests_today = messages_result.scalar() or 0
    
    # Count active subscriptions
    subs_result = await db.execute(
        select(func.count(Subscription.id))
        .where(Subscription.status == "active")
    )
    active_subscriptions = subs_result.scalar() or 0
    
    # Calculate revenue (mock for now)
    revenue_mtd = 84290.50
    
    return DashboardMetrics(
        total_users=total_users,
        active_agents=active_agents,
        total_conversations=total_conversations,
        api_requests_today=api_requests_today,
        revenue_mtd=revenue_mtd,
        active_subscriptions=active_subscriptions
    )


@router.get("/usage", response_model=List[UsageMetrics])
async def get_usage_metrics(
    period: str = Query(default="7d", pattern="^(7d|30d|90d)$"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get usage metrics for a period."""
    days = {"7d": 7, "30d": 30, "90d": 90}[period]
    metrics = []
    
    for i in range(days):
        date = datetime.utcnow() - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        
        # Count messages for this day
        day_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
        day_end = day_start + timedelta(days=1)
        
        messages_result = await db.execute(
            select(func.count(Message.id))
            .where(
                Message.created_at >= day_start,
                Message.created_at < day_end
            )
        )
        messages_count = messages_result.scalar() or 0
        
        metrics.append(UsageMetrics(
            date=date_str,
            messages_count=messages_count,
            tokens_used=messages_count * 100,  # Estimate
            active_users=min(messages_count // 10, 100),  # Estimate
            agents_executed=min(messages_count // 20, 50)  # Estimate
        ))
    
    return list(reversed(metrics))  # Return oldest first


@router.get("/revenue")
async def get_revenue_metrics(
    period: str = Query(default="30d", pattern="^(7d|30d|90d|1y)$"),
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get revenue metrics."""
    # In production, calculate from actual billing data
    return {
        "total_revenue": 125000.00,
        "revenue_growth": 15.5,
        "monthly_recurring_revenue": 84290.50,
        "average_revenue_per_user": 49.99,
        "churn_rate": 2.3,
        "projections": {
            "next_month": 90000.00,
            "next_quarter": 270000.00,
            "next_year": 1100000.00
        }
    }


@router.get("/users")
async def get_user_analytics(
    current_user: User = Depends(require_admin),
    db: AsyncSession = Depends(get_db)
):
    """Get user analytics."""
    # Get user counts by plan
    free_users = await db.execute(
        select(func.count(User.id))
        .where(User.subscription_plan == "free")
    )
    pro_users = await db.execute(
        select(func.count(User.id))
        .where(User.subscription_plan == "pro")
    )
    business_users = await db.execute(
        select(func.count(User.id))
        .where(User.subscription_plan == "business")
    )
    enterprise_users = await db.execute(
        select(func.count(User.id))
        .where(User.subscription_plan == "enterprise")
    )
    
    # Get new users in last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    new_users = await db.execute(
        select(func.count(User.id))
        .where(User.created_at >= thirty_days_ago)
    )
    
    return {
        "total_users": {
            "free": free_users.scalar() or 0,
            "pro": pro_users.scalar() or 0,
            "business": business_users.scalar() or 0,
            "enterprise": enterprise_users.scalar() or 0
        },
        "new_users_last_30_days": new_users.scalar() or 0,
        "active_users_today": 847,
        " Retention rate 30d": 78.5
    }