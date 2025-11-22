from .state import CodeState
from .models.geminiIterativo import *
from .models.geminiRecursivo import *
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage


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