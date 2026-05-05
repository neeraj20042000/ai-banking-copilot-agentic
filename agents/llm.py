import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

def call_llm(prompt: str, max_tokens: int = 300):
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
        temperature=0.3
    )

    return response.choices[0].message.content