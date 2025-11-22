from langchain.tools import tool
from sympy import sympify
from sympy.abc import i, j, k, n


# implementar las tools
@tool
def convertir_a_sumatoria(codigo: list) -> str:
    """
    Tool responsable por convertir un codigo representado en forma de grafo/arbol a una sumatoria matematica lista para ser procesada por sympy
    """

    def procesar_bloque(bloque: dict, nivel: int = 0) -> str:
        """Convierte un codigo representado en forma de grafo/arbol a una sumatoria matematica usando SymPy
        Procesa recursivamente un bloque de código y genera expresiones SymPy
        """
        terminos = []
        indices = [i, j, k]  # Diferentes índices para niveles anidados
        indice_actual = indices[nivel % len(indices)]

        for key, value in bloque.items():
            # Manejar ciclos FOR
            if isinstance(key, tuple) and key[0] == "for":
                iteraciones = key[1]
                try:
                    limite = sympify(iteraciones)
                except:
                    limite = n

                if value:  # Si hay código dentro del for
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    if contenido_interno:
                        terminos.append(
                            f"Sum({contenido_interno}, ({indice_actual.name}, 1, {limite}))"
                        )
                    else:
                        terminos.append(f"Sum(1, ({indice_actual.name}, 1, {limite}))")
                else:
                    terminos.append(f"Sum(1, ({indice_actual.name}, 1, {limite}))")

            # Manejar ciclos WHILE
            elif isinstance(key, tuple) and key[0] == "while":
                condicion = key[1]
                if value:
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    terminos.append(
                        f"W_{{{condicion}}}*({contenido_interno if contenido_interno else '1'})"
                    )
                else:
                    terminos.append(f"W_{{{condicion}}}")

            # Manejar condicionales IF
            elif isinstance(key, tuple) and key[0] == "if":
                if value:
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    terminos.append(
                        f"({contenido_interno if contenido_interno else '1'})"
                    )
                else:
                    terminos.append("1")

            # Manejar ELSE
            elif key == "else":
                if value:
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    terminos.append(
                        f"({contenido_interno if contenido_interno else '1'})"
                    )
                else:
                    terminos.append("1")

            # Manejar llamadas a funciones
            elif key == "func_call":
                func_name = value[0]
                params = value[1]
                # Extraer tamaños de los parámetros
                param_sizes = []
                for param in params:
                    if param[1]:  # Si tiene tamaño definido
                        param_sizes.append(param[1].strip("[]"))

                if param_sizes:
                    terminos.append(f"T_{func_name}({', '.join(param_sizes)})")
                else:
                    terminos.append(f"T_{func_name}(n)")

        # Combinar términos con suma
        if terminos:
            return " + ".join(terminos)
        return ""

    def procesar_funciones(lista_codigo: list) -> str:
        """
        Procesa la lista de funciones y genera sumatorias SymPy para cada una
        """
        ecuaciones = []

        for func_dict in lista_codigo:
            for func_name, func_data in func_dict.items():
                variables = func_data.get("variables", [])
                code = func_data.get("code", {})

                # Obtener parámetros de entrada
                params = []
                for var in variables:
                    if var[1]:  # Si tiene tamaño
                        params.append(var[1].strip("[]"))

                param_str = ", ".join(params) if params else "n"

                # Procesar el código de la función
                sumatoria = procesar_bloque(code)

                if sumatoria:
                    ecuaciones.append(f"T_{func_name}({param_str}) = {sumatoria}")
                else:
                    ecuaciones.append(f"T_{func_name}({param_str}) = 1")

        return "\n".join(ecuaciones)

    resultado = procesar_funciones(codigo)
    return resultado


@tool
def calcular_costo_funcion_temporal(sumatoria: str) -> str:
    """
    Calcula la sumatoria dada y retorna su resultado simplificado
    """
    expr = sympify(sumatoria)
    return expr.doit()
