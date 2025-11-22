import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import ToolNode
from ..tools.toolsIterativas import convertir_a_sumatoria, calcular_costo_funcion_temporal


dotenv.load_dotenv()

gemini_iterativo = ChatGoogleGenerativeAI(
    model=os.environ.get("MODEL", "gemini-2.5-flash"), 
    api_key=os.environ["GEMINI_API_KEY"]
)

tools_iterativo = [convertir_a_sumatoria, calcular_costo_funcion_temporal]

gemini_iterativo_with_tools = gemini_iterativo.bind_tools(tools_iterativo)

tools_node_iterativo = ToolNode(tools_iterativo, name="tools_iterativo")