from agents.state import AgentState
from guardrails.moderation import check_toxicity


def guardrail_agent(state: AgentState) -> AgentState:
    """Perform pre guardrail checks on the incoming query and short-circuit unsafe input."""
    query = state.get("query", "")
    if check_toxicity(query):
        state["response"] = '''Unsafe or inappropriate words detected, please try another query. 
        This response is system-generated and may not always be accurate or complete. '''
    return state
