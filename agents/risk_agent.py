from agents.llm import call_llm

def risk_agent(customer_context: str):
    prompt = f"""
    Evaluate financial risk based on context.

    Context: {customer_context}

    Return:
    - risk_level (low/medium/high)
    - reasoning
    """

    return call_llm(prompt, max_tokens=150)