from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def ask_ai(message):
    if not message:
        return "Please enter a question."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a travel assistant."},
                {"role": "user", "content": message}
            ],
            max_tokens=250
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return f"OpenAI error: {e}"
