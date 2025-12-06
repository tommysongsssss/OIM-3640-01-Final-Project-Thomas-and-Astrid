from openai import OpenAI
from config import Config

# Initialize OpenAI client
client = OpenAI(api_key=Config.OPENAI_API_KEY)


def ask_ai(question, context=""):
    """
    Ask OpenAI a question with optional trip context.
    """

    prompt = f"""
You are a friendly and helpful travel planning assistant.

Trip Context:
{context}

User Question:
{question}

Give a clear and helpful answer.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )

    return response.choices[0].message.content