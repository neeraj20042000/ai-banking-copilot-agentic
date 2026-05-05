from agents.llm import call_llm
from agents.state import AgentState

def risk_agent(state: AgentState) -> AgentState:
    loan = state["loan_result"]
    prompt = f"Evaluate credit risk based on: {loan}. Output: LOW / MEDIUM / HIGH with reason."
    result = call_llm(prompt, max_tokens=150)
    state["risk_result"] = result
    return state
