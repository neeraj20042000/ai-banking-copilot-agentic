from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class AgentStateSnapshot(BaseModel):
    """Snapshot of agent state before/after execution."""
    query: Optional[str] = None
    intent: Optional[str] = None
    user_data: Optional[Dict[str, Any]] = None
    loan_result: Optional[Dict] = None
    risk_result: Optional[str] = None
    rag_context: Optional[str] = None
    response: Optional[str] = None
    short_term_context: Optional[str] = None
    long_term_context: Optional[str] = None


class AgentProgress(BaseModel):
    """Tracks progress of a single agent execution."""
    agent_name: str
    state_before: AgentStateSnapshot
    state_after: AgentStateSnapshot


class QueryResponse(BaseModel):    
    # Agent execution tracking
    user_id: Optional[str] = None
    current_agent: Optional[str] = None
    progress: Optional[List[AgentProgress]] = None