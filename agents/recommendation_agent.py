from agents.llm import call_llm

def recommendation_agent(context: str):
    prompt = f"""
    Provide financial recommendation.

    Context: {context}

    Return:
    - recommendation
    - justification
    """

    return call_llm(prompt, max_tokens=200)