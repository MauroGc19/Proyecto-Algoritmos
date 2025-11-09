from .tools import *

from typing import TypedDict, Annotated, Literal

import os
import dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

dotenv.load_dotenv()

class CodeState(TypedDict):
    code: Annotated[str, "Codigo original, a ser compilado y estudiado"]
    mermaid_graph: Annotated[str, "Codigo simplificado, sera utilizado para estudiar y sacar las eficiencias"]
    type: Annotated[Literal["RECURSIVO", "ITERATIVO", "ERROR"], "Tipo de codigo: 'RECURSIVO', 'ITERATIVO', 'ERROR'"]
    eficiencia_t: Annotated[str, "Eficiencia temporal del codigo"]
    eficiencia_e: Annotated[str, "Eficiencia espacial del codigo"]

# Modelo para código recursivo
gemini_recursivo = ChatGoogleGenerativeAI(
    model=os.environ.get("MODEL", "gemini-2.5-flash"), 
    api_key=os.environ["GEMINI_API_KEY"]
)

# Modelo para código iterativo
gemini_iterativo = ChatGoogleGenerativeAI(
    model=os.environ.get("MODEL", "gemini-2.5-flash"), 
    api_key=os.environ["GEMINI_API_KEY"]
)

# Herramientas específicas para cada tipo
tools_recursivo = []  # Herramientas para recursivos
tools_iterativo = []  # Herramientas para iterativos

# Bind tools a cada modelo
gemini_recursivo_with_tools = gemini_recursivo.bind_tools(tools_recursivo)
gemini_iterativo_with_tools = gemini_iterativo.bind_tools(tools_iterativo)

tools_node_recursivo = ToolNode(tools_recursivo, name="tools_recursivo")
tools_node_iterativo = ToolNode(tools_iterativo, name="tools_iterativo")

# nodos
def compilar_codigo_node(state: CodeState) -> CodeState:
    return state

def analizar_codigo_node(state: CodeState) -> CodeState:
    return state

def analisador_patrones_recursivo_node(state: CodeState) -> CodeState:
    return state

def analisador_patrones_iterativo_node(state: CodeState) -> CodeState:
    return state

def aplicar_metodos_analisis_recursivo_node(state: CodeState) -> CodeState:
    return state

def aplicar_metodos_analisis_iterativo_node(state: CodeState) -> CodeState:
    return state

def preparar_salida_node(state: CodeState) -> CodeState:
    return state
    

# Grafo de estados
graph_builder = StateGraph(CodeState)

# Nodos
graph_builder.add_node("compilar_codigo", compilar_codigo_node)
graph_builder.add_node("analizar_codigo", analizar_codigo_node)
graph_builder.add_node("analisador_patrones_recursivo", analisador_patrones_recursivo_node)
graph_builder.add_node("analisador_patrones_iterativo", analisador_patrones_iterativo_node)
graph_builder.add_node("aplicar_metodos_analisis_recursivo", aplicar_metodos_analisis_recursivo_node)
graph_builder.add_node("aplicar_metodos_analisis_iterativo", aplicar_metodos_analisis_iterativo_node)
graph_builder.add_node("preparar_salida", preparar_salida_node)


# Edges
graph_builder.add_edge(START, "compilar_codigo")
graph_builder.add_edge("compilar_codigo", "analizar_codigo")
graph_builder.add_edge("analisador_patrones_recursivo", "aplicar_metodos_analisis_recursivo")
graph_builder.add_edge("analisador_patrones_iterativo", "aplicar_metodos_analisis_iterativo")
graph_builder.add_edge("aplicar_metodos_analisis_recursivo", "preparar_salida")
graph_builder.add_edge("aplicar_metodos_analisis_iterativo", "preparar_salida")
graph_builder.add_edge("preparar_salida", END)

# Conditional edges
def conditional_edge_analizar_codigo(state: CodeState) -> str:
    return state["type"]

graph_builder.add_conditional_edges(                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
    "analizar_codigo",
    conditional_edge_analizar_codigo,
    {
        "RECURSIVO": "analisador_patrones_recursivo",
        "ITERATIVO": "analisador_patrones_iterativo",
        "ERROR": "preparar_salida"
    },
)

agent_graph = graph_builder.compile()