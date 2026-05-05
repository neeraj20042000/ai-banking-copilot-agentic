from agents.llm import call_llm
from agents.state import AgentState


def recommendation_agent(state: AgentState) -> AgentState:
    """Generate financial recommendation based on user query and context"""
    context = state.get("rag_context", "")
    query = state["query"]
    
    # Use long-term memory context for personalization (short-term not needed for single-turn queries)
    long_term_context = state.get("long_term_context", "")
    
    # Build prompt with memory context for personalization
    prompt_parts = [f"User Query: {query}"]
    
    if context:
        prompt_parts.append(f"Context: {context}")
    
    if long_term_context:
        prompt_parts.append(f"User Profile & Preferences:\n{long_term_context}")
    
    prompt = "\n\n".join(prompt_parts) + "\n\nProvide personalized financial recommendation based on user profile and preferences."
    
    response = call_llm(prompt)
    state["response"] = response
    
    # Store conversation in state for later persistence
    state["_conversation_to_save"] = {
        "user": query,
        "assistant": response[:200] + "..." if len(response) > 200 else response
    }
    
    # Extract keywords and takeaways in a single LLM call for efficiency
    memory_prompt = f"""Analyze this conversation and extract key information for long-term memory.

User Query: {query}
Response: {response}

Return a JSON object with exactly this format:
{{"keywords": "keyword1, keyword2, keyword3 OR none", "takeaway": "short phrase OR none"}}

- keywords: 2-3 important keywords representing user interests or preferences (comma-separated)
- takeaway: 1 important takeaway about the user (preferences, needs, or constraints) in max 10 words"""

    memory_result = call_llm(memory_prompt, max_tokens=80).strip()
    
    # Parse the JSON response
    try:
        import json
        # Try to extract JSON from response
        if "{" in memory_result and "}" in memory_result:
            json_start = memory_result.find("{")
            json_end = memory_result.rfind("}") + 1
            memory_data = json.loads(memory_result[json_start:json_end])
        else:
            memory_data = {"keywords": "none", "takeaway": "none"}
        
        # Extract keywords
        keywords = memory_data.get("keywords", "").strip()
        if keywords and keywords.lower() != "none":
            state["_keywords_to_save"] = [kw.strip() for kw in keywords.split(",")]
        
        # Extract takeaway
        takeaway = memory_data.get("takeaway", "").strip()
        if takeaway and takeaway.lower() != "none":
            state["_takeaway_to_save"] = takeaway
            
    except (json.JSONDecodeError, ValueError):
        pass  # Silently skip if parsing fails
    
    return state
