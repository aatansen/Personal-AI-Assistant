import os
from dotenv import load_dotenv

class Settings:
    def load_api_key(self):
        load_dotenv()
        key = os.getenv("GEMINI_API_KEY")
        if not key:
            raise EnvironmentError("GEMINI_API_KEY not found")
        return key
