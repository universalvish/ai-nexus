"""AI Agent API endpoints."""

from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_db
from app.schemas import (
    AgentCreate, AgentUpdate, AgentResponse, 
    AgentExecuteRequest, AgentExecutionResponse,
    SuccessResponse, PaginatedResponse
)
from app.api.deps import get_current_user, require_admin
from app.models import User, Agent, AgentExecution
from app.core.enums import AgentStatus, MessageRole

router = APIRouter(prefix="/agents", tags=["AI Agents"])


@router.get("", response_model=List[AgentResponse])
async def list_agents(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all agents for current user."""
    result = await db.execute(
        select(Agent)
        .where(Agent.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    agents = result.scalars().all()
    return [AgentResponse.model_validate(agent) for agent in agents]


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    agent_data: AgentCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new AI agent."""
    agent = Agent(
        user_id=current_user.id,
        name=agent_data.name,
        description=agent_data.description,
        agent_type=agent_data.agent_type,
        configuration=agent_data.configuration,
        system_prompt=agent_data.system_prompt,
        tools=agent_data.tools,
        memory_enabled=agent_data.memory_enabled,
        status=AgentStatus.IDLE
    )
    db.add(agent)
    await db.flush()
    
    return AgentResponse.model_validate(agent)


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific agent."""
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == current_user.id
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    return AgentResponse.model_validate(agent)


@router.patch("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update an agent."""
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == current_user.id
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Update fields
    update_data = agent_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            setattr(agent, field, value)
    
    await db.flush()
    return AgentResponse.model_validate(agent)


@router.delete("/{agent_id}", response_model=SuccessResponse)
async def delete_agent(
    agent_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete an agent."""
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == current_user.id
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    await db.delete(agent)
    await db.flush()
    
    return SuccessResponse(message="Agent deleted")


@router.post("/{agent_id}/execute", response_model=AgentExecutionResponse)
async def execute_agent(
    agent_id: int,
    request: AgentExecuteRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Execute an agent action."""
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == current_user.id
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    if not agent.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Agent is not active"
        )
    
    # Create execution record
    execution = AgentExecution(
        agent_id=agent_id,
        action=request.action,
        input_data=request.params,
        status="pending"
    )
    db.add(execution)
    await db.flush()
    
    # Update agent status
    agent.status = AgentStatus.ACTIVE
    agent.last_active_at = datetime.utcnow()
    
    try:
        # Simulate execution (in production, this would run the actual agent)
        # For demo, we'll simulate a response
        output_data = {
            "result": f"Executed {request.action} successfully",
            "action": request.action,
            "params": request.params
        }
        
        execution.output_data = output_data
        execution.status = "success"
        execution.execution_time_ms = 150
        
        # Update agent stats
        agent.tasks_completed += 1
        agent.status = AgentStatus.IDLE
        
    except Exception as e:
        execution.status = "failed"
        execution.error_message = str(e)
        agent.status = AgentStatus.ERROR
    
    await db.flush()
    
    return AgentExecutionResponse.model_validate(execution)


@router.get("/{agent_id}/executions", response_model=List[AgentExecutionResponse])
async def get_agent_executions(
    agent_id: int,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get execution history for an agent."""
    # Verify ownership
    result = await db.execute(
        select(Agent).where(
            Agent.id == agent_id,
            Agent.user_id == current_user.id
        )
    )
    agent = result.scalar_one_or_none()
    
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # Get executions
    result = await db.execute(
        select(AgentExecution)
        .where(AgentExecution.agent_id == agent_id)
        .order_by(AgentExecution.created_at.desc())
        .limit(limit)
    )
    executions = result.scalars().all()
    
    return [AgentExecutionResponse.model_validate(e) for e in executions]