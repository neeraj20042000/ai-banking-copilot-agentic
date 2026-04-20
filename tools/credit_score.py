def check_credit_score(score: int):
    if score >= 750:
        return "Excellent - Eligible for best loan offers"
    elif score >= 650:
        return "Good - Eligible with moderate interest"
    else:
        return "Low - Risky borrower"