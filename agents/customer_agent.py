from agents.llm import call_llm

def customer_agent(user_query: str):
    prompt = f"""
    Extract key financial intent from the query.

    Query: {user_query}

    Return JSON:
    - intent
    - user_need
    """

    return call_llm(prompt, max_tokens=150)