from langgraph.graph import StateGraph, END
from agents.state import AgentState

from agents.intent_agent import intent_agent
from agents.risk_agent import risk_agent
from agents.recommendation_agent import recommendation_agent
from agents.compliance_agent import compliance_agent
from agents.guardrail_agent import guardrail_agent
from agents.loan_agent import loan_agent
from agents.rag_agent import rag_agent


# ---- STATE SNAPSHOT UTILS ---- #

def _snapshot_state(state: AgentState) -> dict:
    """Create a snapshot of the current agent state."""
    return {
        "query": state.get("query"),
        "intent": state.get("intent"),
        "user_data": state.get("user_data"),
        "loan_result": state.get("loan_result"),
        "risk_result": state.get("risk_result"),
        "rag_context": state.get("rag_context"),
        "response": state.get("response"),
        "short_term_context": state.get("short_term_context"),
        "long_term_context": state.get("long_term_context"),
    }


def _create_tracked_agent(agent_fn, agent_name: str):
    """Wrap an agent function to track state before/after execution."""
    def tracked_agent(state: AgentState) -> AgentState:
        # Capture state before execution - create new dict to avoid reference issues
        state_before = _snapshot_state(state)
        
        # Execute the agent - handle both in-place modification and return value
        result = agent_fn(state)
        
        # Handle case where agent returns partial state vs modifies in-place
        if isinstance(result, dict):
            state = {**state, **result}
        
        # Store progress - create new list to avoid shared reference issues
        progress = list(state.get("_progress", []))
        progress.append({
            "agent_name": agent_name,
            "state_before": state_before,
            "state_after": _snapshot_state(state)
        })
        state["_progress"] = progress
        state["_current_agent"] = agent_name
           
        return state
    return tracked_agent


# ---- ROUTER ---- #

def route_after_guardrail(state: AgentState):
    """Route to intent if query is safe, or end directly if unsafe (toxic query detected)"""
    if state.get("response"):
        return "END"
    return "intent"


def route_intent(state: AgentState):
    """Route to loan or recommendation flow based on identified intent"""
    intent = state["intent"]
    if intent == "loan":
        return "loan_calc"
    else:
        return "rag"

# ---- BUILD GRAPH ---- #

def build_graph():
    graph = StateGraph(AgentState)
    
    # Wrap agents with tracking
    graph.add_node("guardrail", _create_tracked_agent(guardrail_agent, "guardrail"))
    graph.add_node("intent", _create_tracked_agent(intent_agent, "intent"))
    graph.add_node("loan_calc", _create_tracked_agent(loan_agent, "loan_calc"))
    graph.add_node("risk", _create_tracked_agent(risk_agent, "risk"))
    graph.add_node("rag", _create_tracked_agent(rag_agent, "rag"))
    graph.add_node("recommend", _create_tracked_agent(recommendation_agent, "recommend"))
    graph.add_node("compliance", _create_tracked_agent(compliance_agent, "compliance"))
    
    graph.set_entry_point("guardrail")
    graph.add_conditional_edges("guardrail", route_after_guardrail, {"intent": "intent", "END": END})
    graph.add_conditional_edges("intent", route_intent, {"loan_calc": "loan_calc", "rag": "rag"})
    graph.add_edge("loan_calc", "risk")
    graph.add_edge("risk", "compliance")
    graph.add_edge("rag", "recommend")
    graph.add_edge("recommend", "compliance")
    graph.add_edge("compliance", END)
    return graph.compile()
