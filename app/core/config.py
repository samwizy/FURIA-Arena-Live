import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    API_KEY = os.getenv("GEMINI_API_KEY")
    MODEL_NAME = "models/gemini-2.0-flash"

settings = Settings()