from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def get_ai_outfit_recommendation(weather_summary, activities):
    prompt = f"""
Weather:
{weather_summary}

Activities:
{', '.join(activities)}

Give 2–3 outfit recommendations.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=250
    )

    return res.choices[0].message["content"]
