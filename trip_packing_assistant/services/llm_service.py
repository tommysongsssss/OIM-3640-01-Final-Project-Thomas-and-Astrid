from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.OPENAI_API_KEY)

def get_ai_outfit_recommendation(weather_summary, activities):
    """
    Uses OpenAI to generate a creative daily outfit idea.
    """
    if not Config.OPENAI_API_KEY:
        return "AI suggestions unavailable (No API Key found)."

    try:
        activity_str = ", ".join(activities)
        prompt = (
            f"I am traveling to a place with this weather: {weather_summary}. "
            f"My activities are: {activity_str}. "
            "Suggest ONE stylish and practical outfit combination for a typical day."
        )

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful travel fashion assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Could not generate AI outfit suggestion."