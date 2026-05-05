from typing import Dict, Any

def calculate_emi(principal: float, rate: float, tenure: int) -> float:
    """
    Calculate EMI using formula:
    EMI = [P *  r * (1+r)^n] / [(1+r)^n - 1]
    where r is monthly rate and n is tenure in months
    """
    monthly_rate = rate / (12 * 100)
    num_months = tenure * 12
    
    if monthly_rate == 0:
        return principal / num_months
    
    emi = (principal * monthly_rate * (1 + monthly_rate) ** num_months) / \
          ((1 + monthly_rate) ** num_months - 1)
    
    return round(emi, 2)

def calculate_loan_eligibility(
    principal,
    rate,
    tenure,
    income,
    expenses,
    credit_score
) -> Dict[str, Any]:
    """
    Calculate loan eligibility based on banking standards.
    
    Parameters can be numbers or strings containing "example" with numbers.
    All parameters will be converted to appropriate numeric types.
    """
    
    # Convert parameters to numeric types, handling "example" strings
    def extract_number(value):
        if isinstance(value, str) and "example" in value.lower():
            # Extract number from "example: 500000" format
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', value)
            return float(match.group(1)) if match else 0
        return float(value) if value is not None else 0
    
    principal = extract_number(principal)
    rate = extract_number(rate)
    tenure = int(extract_number(tenure))
    income = extract_number(income)
    expenses = extract_number(expenses)
    credit_score = int(extract_number(credit_score))
    
    # Validate credit score
    if credit_score < 650:
        return {
            "eligible": False,
            "reason": "Credit score below minimum threshold (650)",
            "credit_score": credit_score
        }
    
    # Calculate monthly net income
    annual_net_income = income - expenses
    monthly_net_income = annual_net_income / 12
    
    if monthly_net_income <= 0:
        return {
            "eligible": False,
            "reason": "Annual expenses exceed annual income",
            "monthly_net_income": monthly_net_income
        }
    
    # Calculate EMI
    emi = calculate_emi(principal, rate, tenure)
    
    # Calculate EMI/NMI ratio (banking standard: < 0.5)
    emi_nmi_ratio = emi / monthly_net_income
    
    if emi_nmi_ratio >= 0.5:
        return {
            "eligible": False,
            "reason": f"EMI/NMI ratio {emi_nmi_ratio:.2f} exceeds banking standard (0.5)",
            "emi": emi,
            "monthly_net_income": round(monthly_net_income, 2),
            "emi_nmi_ratio": round(emi_nmi_ratio, 2),
            "credit_score": credit_score
        }
    
    # User is eligible
    total_amount_payable = emi * tenure * 12
    
    return {
        "eligible": True,
        "principal": principal,
        "rate_of_interest": rate,
        "tenure_years": tenure,
        "tenure_months": tenure * 12,
        "emi": emi,
        "total_amount_payable": round(total_amount_payable, 2),
        "total_interest": round(total_amount_payable - principal, 2),
        "monthly_net_income": round(monthly_net_income, 2),
        "emi_nmi_ratio": round(emi_nmi_ratio, 2),
        "annual_income": income,
        "annual_expenses": expenses,
        "credit_score": credit_score
    }