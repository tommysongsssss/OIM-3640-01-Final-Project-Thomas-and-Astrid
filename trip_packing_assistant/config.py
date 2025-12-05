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
