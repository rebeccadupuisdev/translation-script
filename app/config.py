import os

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

BASE_URL = "https://www.teanglann.ie/en/fgb/"
AUDIO_URL = "https://www.teanglann.ie/CanC/"
AUDIO_DIR = "audio_files"
