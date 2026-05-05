BANNED_WORDS = [
    "spam",
    "fraud",
    "hate",
    "violence",
]

def check_toxicity(text: str) -> bool:
    cleaned = (text or "").lower()
    return any(word in cleaned for word in BANNED_WORDS)
