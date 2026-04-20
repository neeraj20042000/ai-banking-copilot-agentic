from langchain.tools import Tool
from tools.loan_calculator import calculate_emi
from tools.credit_score import check_credit_score

loan_tool = Tool(
    name="Loan Calculator",
    func=lambda x: calculate_emi(**x),
    description="Calculates EMI based on principal, rate, and tenure"
)

credit_tool = Tool(
    name="Credit Score Checker",
    func=lambda x: check_credit_score(**x),
    description="Evaluates credit score"
)

TOOLS = [loan_tool, credit_tool]