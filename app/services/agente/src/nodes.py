from .state import CodeState
from .models.geminiIterativo import *
from .models.geminiRecursivo import *
from .models.gemini import *
from ....services.analisis_complejidad.src.compilador_lark import compilar_codigo
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, ToolMessage
import json

"""
class CodeState(TypedDict):
    code: Annotated[str, "Codigo original, a ser compilado y estudiado"]
    mermaid_graph: Annotated[str, "Codigo simplificado, sera utilizado para estudiar y sacar las eficiencias"]
    type: Annotated[Literal["RECURSIVO", "ITERATIVO", "ERROR"], "Tipo de codigo: 'RECURSIVO', 'ITERATIVO', 'ERROR'"]
    eficiencia_tO: Annotated[str, "Eficiencia temporal del codigo BIG O"]
    eficiencia_eO: Annotated[str, "Eficiencia espacial del codigo BIG O"]
    eficiencia_tTH: Annotated[str, "Eficiencia temporal del codigo BIG THETA"]
    eficiencia_eTH: Annotated[str, "Eficiencia espacial del codigo BIG THETA"]
    eficiencia_tOM: Annotated[str, "Eficiencia temporal del codigo BIG OMEGA"]
    eficiencia_eOM: Annotated[str, "Eficiencia espacial del codigo BIG OMEGA"]

"""


# nodos
def compilar_codigo_node(state: CodeState) -> CodeState:
    try:
        compilar_codigo(state.get("code", ""))
    except Exception as e:
        print("Error de compilacion:", e)
        state["type"] = "ERROR"
    return state


def analizar_codigo_node(state: CodeState) -> CodeState:
    FILE = "./app/services/agente/prompts/AnalizadorTipoPrompt.md"
    prompt = ""
    with open(FILE, "r") as f:
        prompt = f.read()
    systemMessage = SystemMessage(content=prompt)
    humanMessage = HumanMessage(state["code"])
    respuesta = gemini.invoke([systemMessage, humanMessage])
    response_data = str(respuesta.content)
    parsed_response = json.loads(response_data)
    state["type"] = parsed_response["tipo"].upper()
    state["mermaid_graph"] = json.dumps(parsed_response.get("estructura_codigo", []))
    return state


def analisador_patrones_recursivo_node(state: CodeState) -> CodeState:
    return state


def analisador_patrones_iterativo_node(state: CodeState) -> CodeState:
    # Va a generar las ecuaciones de sumatorias para el mejor, peor y caso promedio
    return state


def aplicar_metodos_analisis_recursivo_node(state: CodeState) -> CodeState:

    return state


def aplicar_metodos_analisis_iterativo_node(state: CodeState) -> CodeState:
    """
    Analiza la complejidad de algoritmos iterativos usando LLM con tools.
    Genera sumatorias y calcula eficiencias para los tres casos.
    """
    FILE = "./app/services/agente/prompts/AnalizadorIterativoPrompt.md"
    prompt = ""
    with open(FILE, "r") as f:
        prompt = f.read()

    # Preparar mensajes
    systemMessage = SystemMessage(content=prompt)
    humanMessage = HumanMessage(
        content=f"Analiza la siguiente estructura de código y determina sus complejidades:\n\n{state['mermaid_graph']}"
    )

    messages = [systemMessage, humanMessage]

    # Ciclo de interacción con el LLM y las tools
    max_iterations = 10
    for _ in range(max_iterations):
        response = gemini_iterativo_with_tools.invoke(messages)
        messages.append(response)

        # Si no hay tool calls, el LLM ha terminado
        if not response.tool_calls:
            break

        # Ejecutar las tools solicitadas
        tool_results = tools_node_iterativo.invoke({"messages": messages})
        messages.extend(tool_results["messages"])

    # Extraer la respuesta final
    final_response = messages[-1].content

    try:
        # Intentar parsear el JSON de respuesta
        if isinstance(final_response, str):
            # Buscar el JSON en la respuesta
            import re

            json_match = re.search(r"\{[\s\S]*\}", final_response)
            if json_match:
                parsed_response = json.loads(json_match.group())

                # Actualizar el estado con las eficiencias
                eficiencia_temporal = parsed_response.get("eficiencia_temporal", {})
                eficiencia_espacial = parsed_response.get("eficiencia_espacial", {})

                state["eficiencia_tOM"] = eficiencia_temporal.get("mejor_caso", "1")
                state["eficiencia_tO"] = eficiencia_temporal.get("peor_caso", "n")
                state["eficiencia_tTH"] = eficiencia_temporal.get(
                    "caso_promedio", "n"
                )

                state["eficiencia_eOM"] = eficiencia_espacial.get("mejor_caso", "1")
                state["eficiencia_eO"] = eficiencia_espacial.get("peor_caso", "n")
                state["eficiencia_eTH"] = eficiencia_espacial.get(
                    "caso_promedio", "n"
                )
    except Exception as e:
        print(f"Error al parsear respuesta del análisis iterativo: {e}")

    return state


def preparar_salida_node(state: CodeState) -> CodeState:
    return state
