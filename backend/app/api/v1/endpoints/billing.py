"""Billing API endpoints."""

from typing import List, Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.schemas import (
    PlanResponse, SubscriptionResponse, CheckoutRequest, InvoiceResponse,
    SuccessResponse
)
from app.api.deps import get_current_user
from app.models import User, Subscription, Invoice
from app.core.enums import SubscriptionPlan, SubscriptionStatus

router = APIRouter(prefix="/billing", tags=["Billing"])


# Mock plans data
MOCK_PLANS = {
    "free": {
        "id": "price_free",
        "name": "Free",
        "description": "Perfect for exploring the platform",
        "price": 0,
        "currency": "USD",
        "interval": "month",
        "features": [
            "5 AI conversations per day",
            "1 AI agent",
            "Basic automation",
            "Community support",
            "7-day chat history"
        ],
        "limits": {
            "daily_messages": 5,
            "agents": 1,
            "chat_history_days": 7
        }
    },
    "pro": {
        "id": "price_pro",
        "name": "Pro",
        "description": "For individuals and small teams",
        "price": 29,
        "currency": "USD",
        "interval": "month",
        "features": [
            "Unlimited AI conversations",
            "10 AI agents",
            "Advanced automation",
            "Priority support",
            "30-day chat history",
            "API access",
            "Custom integrations"
        ],
        "limits": {
            "daily_messages": -1,  # Unlimited
            "agents": 10,
            "chat_history_days": 30
        }
    },
    "business": {
        "id": "price_business",
        "name": "Business",
        "description": "For growing businesses",
        "price": 99,
        "currency": "USD",
        "interval": "month",
        "features": [
            "Everything in Pro",
            "Unlimited AI agents",
            "White-label options",
            "SSO & SAML",
            "Custom AI models",
            "Dedicated support",
            "SLA guarantee"
        ],
        "limits": {
            "daily_messages": -1,
            "agents": -1,
            "chat_history_days": 90
        }
    },
    "enterprise": {
        "id": "price_enterprise",
        "name": "Enterprise",
        "description": "For large organizations",
        "price": 499,
        "currency": "USD",
        "interval": "month",
        "features": [
            "Everything in Business",
            "Custom deployment",
            "On-premise option",
            "Advanced security",
            "Training & onboarding",
            "24/7 support",
            "Unlimited everything"
        ],
        "limits": {
            "daily_messages": -1,
            "agents": -1,
            "chat_history_days": -1
        }
    }
}


@router.get("/plans", response_model=List[PlanResponse])
async def list_plans():
    """List all available subscription plans."""
    plans = [PlanResponse(**plan) for plan in MOCK_PLANS.values()]
    return plans


@router.get("/plans/{plan_id}", response_model=PlanResponse)
async def get_plan(plan_id: str):
    """Get a specific plan."""
    if plan_id not in MOCK_PLANS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Plan not found"
        )
    return PlanResponse(**MOCK_PLANS[plan_id])


@router.get("/subscription", response_model=Optional[SubscriptionResponse])
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's subscription."""
    result = await db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id)
        .order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()
    
    if not subscription:
        return None
    
    return SubscriptionResponse.model_validate(subscription)


@router.post("/checkout")
async def create_checkout(
    request: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a checkout session for subscription."""
    plan_id = request.plan_id
    
    if plan_id not in MOCK_PLANS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid plan ID"
        )
    
    plan = MOCK_PLANS[plan_id]
    
    if plan["price"] == 0:
        # Free plan - just update the user
        current_user.subscription_plan = SubscriptionPlan.FREE
        await db.flush()
        return {"url": "/dashboard?upgraded=true"}
    
    # In production, create Stripe checkout session
    # For demo, return mock checkout URL
    return {
        "url": f"https://checkout.stripe.com/mock?plan={plan_id}",
        "session_id": "cs_test_mock_123"
    }


@router.post("/cancel", response_model=SuccessResponse)
async def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Cancel current subscription."""
    result = await db.execute(
        select(Subscription)
        .where(Subscription.user_id == current_user.id)
        .order_by(Subscription.created_at.desc())
    )
    subscription = result.scalar_one_or_none()
    
    if subscription:
        subscription.status = SubscriptionStatus.CANCELED
        subscription.canceled_at = datetime.utcnow()
        await db.flush()
    
    # Downgrade user to free
    current_user.subscription_plan = SubscriptionPlan.FREE
    
    return SuccessResponse(
        message="Subscription canceled. You will retain access until the end of your billing period."
    )


@router.get("/invoices", response_model=List[InvoiceResponse])
async def list_invoices(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List user's invoices."""
    result = await db.execute(
        select(Invoice)
        .where(Invoice.user_id == current_user.id)
        .order_by(Invoice.created_at.desc())
    )
    invoices = result.scalars().all()
    
    return [InvoiceResponse.model_validate(invoice) for invoice in invoices]


@router.post("/webhook")
async def stripe_webhook(
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    """Handle Stripe webhook events."""
    # In production, verify webhook signature and handle events
    event_type = payload.get("type")
    
    if event_type == "checkout.session.completed":
        # Handle successful checkout
        pass
    elif event_type == "customer.subscription.updated":
        # Handle subscription update
        pass
    elif event_type == "customer.subscription.deleted":
        # Handle subscription cancellation
        pass
    elif event_type == "invoice.payment_failed":
        # Handle failed payment
        pass
    
    return SuccessResponse(message="Webhook processed")