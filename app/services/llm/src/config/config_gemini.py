from google import genai
import os

import dotenv
dotenv.load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.
client = genai.Client(os.getenv("GEMINI_API_KEY"))