from agents.llm import call_llm
from agents.state import AgentState


def intent_agent(state: AgentState) -> AgentState:
    """Use LLM to classify intent as either loan or recommendation"""
    query = state["query"]
    
    # Use memory context injected via state (modular approach)
    short_term_context = state.get("short_term_context", "")
    long_term_context = state.get("long_term_context", "")
    
    # Build context for intent classification
    context_parts = []
    if long_term_context:
        context_parts.append(f"User Profile & Preferences:\n{long_term_context}")
    if short_term_context:
        context_parts.append(f"Recent Conversation:\n{short_term_context}")
    
    context_str = "\n\n".join(context_parts) if context_parts else ""
    
    intent_prompt = f"""Classify the user's intent into ONE of these categories:
- loan: If the user is asking about loans, EMI, loan eligibility, loan calculations, etc.
- recommendation: If the user is asking for financial advice, product recommendations, or general banking guidance.

{context_str}

User Query: {query}

Respond with ONLY the category name (loan or recommendation), nothing else."""
    
    response = call_llm(intent_prompt, max_tokens=10).strip().lower()
    intent = "loan" if "loan" in response else "recommendation"
    state["intent"] = intent
    
    # Store conversation in state for later persistence
    state["_conversation_to_save"] = {"user": query, "assistant": f"Intent identified: {intent}"}
    
    return state
