import json

from agents.llm import call_llm
from agents.state import AgentState
from tools.loan_calculator import calculate_loan_eligibility


def loan_agent(state: AgentState) -> AgentState:
    """Extract loan parameters, calculate eligibility, and attach the result to state."""
    query = state.get("query", "")
    user_data = state.get("user_data", {}) or {}

    extraction_prompt = f"""
Extract loan calculation parameters from the user's query and available data.
If parameters are not provided, use reasonable example values and mark them as \"example: <value>\".

User Query: {query}
Available User Data: {user_data}

Extract these parameters as a JSON object:
- principal: Loan amount (if not found, use \"example: 500000\")
- rate: Annual interest rate in % (if not found, use \"example: 8.5\")
- tenure: Loan tenure in years (if not found, use \"example: 5\")
- income: Annual income (if not found, use \"example: 600000\")
- expenses: Annual expenses (if not found, use \"example: 200000\")
- credit_score: Credit score (if not found, use \"example: 750\")

Return ONLY the JSON object, no other text.
Example format: {{"principal": 500000, "rate": 8.5, "tenure": 5, "income": 600000, "expenses": 200000, "credit_score": 750}}
"""

    try:
        llm_response = call_llm(extraction_prompt, max_tokens=200)
        params = json.loads(llm_response.strip())

        result = calculate_loan_eligibility(
            principal=params["principal"],
            rate=params["rate"],
            tenure=params["tenure"],
            income=params["income"],
            expenses=params["expenses"],
            credit_score=params["credit_score"],
        )

        if any(isinstance(v, str) and "example" in v.lower() for v in params.values()):
            result["note"] = "Some parameters used example values as they were not provided by the user."

    except Exception as e:
        result = {
            "eligible": False,
            "reason": f"Error processing loan parameters: {str(e)}",
        }

    state["loan_result"] = result
    return state
