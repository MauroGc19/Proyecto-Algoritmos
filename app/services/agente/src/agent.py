from .tools.toolsIterativas import *
from .nodes import *

from langgraph.graph import StateGraph, START, END






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