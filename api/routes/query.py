from fastapi import APIRouter
from api.schemas.request import QueryRequest
from api.schemas.response import QueryResponse, AgentProgress, AgentStateSnapshot
from agents.orchestrator import build_graph
from agents.state import AgentState
from memory import (
    get_persistent_context,
    get_conversation_history,
    add_conversation,
    add_session_memory
)

router = APIRouter()


def run_agent_graph(query: str) -> AgentState:
    """Run the agent graph with memory context injected via state."""
    # Get memory context
    history = get_conversation_history()
    short_term_context = "\n".join(
        f"{conv['role'].upper()}: {conv['content']}"
        for conv in history
    ) if history else ""
    long_term_context = get_persistent_context() or ""
    
    # Create initial state with memory context
    initial_state: AgentState = {
        "query": query,
        "short_term_context": short_term_context,
        "long_term_context": long_term_context,
        "_progress": [],
    }
    
    # Run graph
    graph = build_graph()
    result = graph.invoke(initial_state)
    
    # Persist memory after graph completes
    _persist_from_state(result)
    
    return result


def _persist_from_state(state: AgentState) -> None:
    """Persist conversation, keywords, and takeaways to memory."""
    # Save conversation to short-term memory
    if state.get("_conversation_to_save"):
        conv = state["_conversation_to_save"]
        add_conversation("user", conv.get("user", ""))
        add_conversation("assistant", conv.get("assistant", ""))
    
    # Save keywords and takeaway to long-term memory in a single call
    keywords = state.get("_keywords_to_save")
    takeaway = state.get("_takeaway_to_save")
    if keywords or takeaway:
        add_session_memory(keywords=keywords, takeaway=takeaway)


def _build_progress_list(progress_data: list) -> list[AgentProgress]:
    """Convert raw progress data to AgentProgress objects."""
    return [
        AgentProgress(
            agent_name=p["agent_name"],
            state_before=AgentStateSnapshot(**p["state_before"]),
            state_after=AgentStateSnapshot(**p["state_after"]),
        )
        for p in progress_data
    ]


@router.post("/query", response_model=QueryResponse)
def process_query(request: QueryRequest):
    
    # Step 1: Extract user input
    user_query = request.query
    user_id = request.user_id

    # Step 2: Run agent graph with memory context
    result = run_agent_graph(user_query)
   
    # Step 3: Build progress list
    progress_data = result.get("_progress", [])
    progress = _build_progress_list(progress_data) if progress_data else None
    
    # Get current agent from last execution
    current_agent = result.get("_current_agent")

    # Step 5: Return structured response
    return QueryResponse(
        user_id=user_id,
        current_agent=current_agent,
        progress=progress,
    )
