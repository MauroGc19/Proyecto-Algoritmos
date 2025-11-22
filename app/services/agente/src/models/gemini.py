import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


dotenv.load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model=os.environ.get("MODEL", "gemini-2.5-flash"), 
    api_key=os.environ["GEMINI_API_KEY"]
)