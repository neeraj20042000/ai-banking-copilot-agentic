from groq import Groq
from config.settings import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY))

def call_llm(prompt: str, max_tokens: int = 300, temperature: float = 0.3):
    """
    Generic LLM caller with strict token control
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a helpful banking AI assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,   # LIMIT TOKENS
        temperature=temperature
    )

    return response.choices[0].message.content