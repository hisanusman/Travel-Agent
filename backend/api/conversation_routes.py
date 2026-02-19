"""
Conversation API Routes
Handles conversational travel planning flow
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from backend.conversation.state import (
    ConversationContext, 
    create_conversation, 
    get_conversation,
    save_conversation
)
from backend.conversation.agent import ConversationAgent
from backend.agents.orchestrator import orchestrator
from loguru import logger

router = APIRouter(prefix="/api/v1/conversation", tags=["conversation"])

# Initialize conversation agent
conversation_agent = ConversationAgent()


class StartConversationRequest(BaseModel):
    """Request to start a new conversation"""
    initial_message: Optional[str] = None


class SendMessageRequest(BaseModel):
    """Request to send a message in conversation"""
    message: str


class ConversationResponse(BaseModel):
    """Response from conversation"""
    conversation_id: str
    agent_message: str
    question: Optional[str]
    suggestions: Optional[List[str]]
    profile: Dict[str, Any]
    completeness: int
    is_ready: bool
    state: str


@router.post("/start", response_model=ConversationResponse)
async def start_conversation(request: StartConversationRequest):
    """
    Start a new conversation
    """
    try:
        # Create new conversation
        context = create_conversation()
        logger.info(f"Started new conversation: {context.conversation_id}")
        
        # Generate greeting
        greeting = await conversation_agent.generate_initial_greeting()
        context.add_message('agent', greeting)
        
        # If user provided initial message, process it
        if request.initial_message:
            response = await conversation_agent.process_message(
                request.initial_message,
                context
            )
            save_conversation(context)
            
            return ConversationResponse(
                conversation_id=context.conversation_id,
                agent_message=response.get('message', ''),
                question=response.get('question'),
                suggestions=response.get('suggestions'),
                profile=context.profile,
                completeness=context.completeness,
                is_ready=context.is_ready_to_plan(),
                state=context.state.value
            )
        
        # Return greeting only
        save_conversation(context)
        return ConversationResponse(
            conversation_id=context.conversation_id,
            agent_message=greeting,
            question="Where would you like to go?",
            suggestions=["Europe", "Beach destination", "City break", "Mountain retreat"],
            profile=context.profile,
            completeness=0,
            is_ready=False,
            state=context.state.value
        )
        
    except Exception as e:
        logger.error(f"Error starting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/message", response_model=ConversationResponse)
async def send_message(conversation_id: str, request: SendMessageRequest):
    """
    Send a message in an existing conversation
    """
    try:
        # Get conversation
        context = get_conversation(conversation_id)
        if not context:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Process message
        response = await conversation_agent.process_message(
            request.message,
            context
        )
        
        # Save updated context
        save_conversation(context)
        
        return ConversationResponse(
            conversation_id=context.conversation_id,
            agent_message=response.get('message', ''),
            question=response.get('question'),
            suggestions=response.get('suggestions'),
            profile=context.profile,
            completeness=context.completeness,
            is_ready=context.is_ready_to_plan(),
            state=context.state.value
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{conversation_id}/finalize")
async def finalize_plan(conversation_id: str):
    """
    Generate final travel plan from conversation
    """
    try:
        # Get conversation
        context = get_conversation(conversation_id)
        if not context:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Check if ready
        if not context.is_ready_to_plan():
            raise HTTPException(
                status_code=400,
                detail=f"Missing required information: {', '.join(context.get_missing_info())}"
            )
        
        # Build user request from context
        destination = context.profile.get('destination')
        if isinstance(destination, list):
            destination = ', '.join(destination)
        
        duration = context.profile.get('duration', 7)
        budget = context.profile.get('budget', 'moderate')
        interests = context.profile.get('interests', [])
        if isinstance(interests, list):
            interests_str = ', '.join(interests)
        else:
            interests_str = str(interests)
        
        # Build natural language request
        user_request = f"{duration} day trip to {destination}"
        if budget:
            user_request += f" with {budget} budget"
        if interests_str:
            user_request += f" interested in {interests_str}"
        
        # Create full travel plan using orchestrator
        logger.info(f"Generating plan for conversation {conversation_id}: {user_request}")
        plan_result = await orchestrator.create_travel_plan(user_request)
        
        # Update context state
        context.state = 'completed'
        save_conversation(context)
        
        return {
            "success": True,
            "conversation_id": conversation_id,
            "plan": plan_result.get('plan'),
            "trip_id": plan_result.get('trip_id')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error finalizing plan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{conversation_id}")
async def get_conversation_details(conversation_id: str):
    """
    Get conversation history and current state
    """
    try:
        context = get_conversation(conversation_id)
        if not context:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return context.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))
