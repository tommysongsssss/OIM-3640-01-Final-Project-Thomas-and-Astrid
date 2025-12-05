import os
from dotenv import load_dotenv

# This command loads the .env file
load_dotenv()

class Config:
    # It tries to get the key from the environment
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')

# --- Packing Logic Thresholds ---
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