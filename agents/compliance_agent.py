from agents.llm import call_llm
from guardrails.compliance import apply_compliance
from guardrails.moderation import check_toxicity
from agents.state import AgentState

def compliance_agent(state: AgentState) -> AgentState:
    response = state.get("response", "")
    risk = state.get("risk_result", "")
    prompt = f"""Ensure this response is compliant with banking regulations.
Response: {response}
Risk: {risk}
Add disclaimer if needed."""
    final = call_llm(prompt)
    if check_toxicity(final):
        final = "Unsafe content detected."
    final = apply_compliance(final)
    state["response"] = final
    return state
