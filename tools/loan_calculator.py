def calculate_emi(principal: float, rate: float, tenure: int):
    """
    Calculate EMI using formula:
    EMI = [P * r * (1+r)^n] / [(1+r)^n - 1]
    """
    monthly_rate = rate / (12 * 100)
    emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure) / \
          ((1 + monthly_rate) ** tenure - 1)

    return {
        "principal": principal,
        "emi": round(emi, 2),
        "total_payment": round(emi * tenure, 2)
    }