import os
from dotenv import load_dotenv

# Load variables from .env (must be in the same folder as app.py)
load_dotenv()


class Config:
    # API keys
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    # Flask secret key
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

    # Flask config
    DEBUG = True

    # --- Packing Logic Thresholds ---
# These are the variables your weather service was looking for!
TEMP_HOT = 25  
TEMP_COLD = 10 
RAIN_THRESHOLD = 0.4 

# --- Activity Options ---
ACTIVITY_CHOICES = {
    'A': 'City sightseeing',
    'B': 'Hiking or outdoor excursions',
    'C': 'Business meetings or formal events',
    'D': 'Sports (Volleyball/Gym)',
    'E': 'Beach or pool vacation'
}