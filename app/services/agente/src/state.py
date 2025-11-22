from typing import TypedDict, Annotated, Literal

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