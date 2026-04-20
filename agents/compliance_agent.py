from agents.llm import call_llm

def compliance_agent(response: str):
    prompt = f"""
    Check if the response is safe and compliant for banking.

    Response: {response}

    Return:
    - is_safe (yes/no)
    - corrected_response (if unsafe)
    """

    return call_llm(prompt, max_tokens=100)