import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode


dotenv.load_dotenv()

# Modelo para código recursivo
gemini_recursivo = ChatGoogleGenerativeAI(
    model=os.environ.get("MODEL", "gemini-2.5-flash"), 
    api_key=os.environ["GEMINI_API_KEY"]
)

# Modelo para código iterativo


# Herramientas específicas para cada tipo
tools_recursivo = []  # Herramientas para recursivos

# Bind tools a cada modelo
gemini_recursivo_with_tools = gemini_recursivo.bind_tools(tools_recursivo)

tools_node_recursivo = ToolNode(tools_recursivo, name="tools_recursivo")
