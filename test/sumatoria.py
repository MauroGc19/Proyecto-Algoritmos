# def convertir_a_sumatoria(codigo: list) -> str:
#     """
#     Convierte un codigo representado en forma de grafo/arbol a una sumatoria matematica usando sintaxis de SymPy
#     """
    
#     def procesar_bloque(bloque: dict, nivel: int = 0, indice_base: str = "i") -> str:
#         """
#         Procesa recursivamente un bloque de código y genera la sumatoria en formato SymPy
#         """
#         terminos = []
#         contador_indice = 0
        
#         for key, value in bloque.items():
#             # Manejar ciclos FOR
#             if isinstance(key, tuple) and key[0] == "for":
#                 iteraciones = key[1]
#                 # Generar un índice único para este nivel
#                 indice = f"{indice_base}{contador_indice}" if nivel > 0 else "i"
#                 contador_indice += 1
                
#                 if value:  # Si hay código dentro del for
#                     contenido_interno = procesar_bloque(value, nivel + 1, indice)
#                     if contenido_interno:
#                         terminos.append(f"Sum({contenido_interno}, ({indice}, 1, {iteraciones}))")
#                     else:
#                         terminos.append(f"Sum(1, ({indice}, 1, {iteraciones}))")
#                 else:
#                     terminos.append(f"Sum(1, ({indice}, 1, {iteraciones}))")
            
#             # Manejar ciclos WHILE
#             elif isinstance(key, tuple) and key[0] == "while":
#                 condicion = key[1]
#                 if value:
#                     contenido_interno = procesar_bloque(value, nivel + 1, indice_base)
#                     terminos.append(f"W_{condicion}*({contenido_interno if contenido_interno else '1'})")
#                 else:
#                     terminos.append(f"W_{condicion}")
            
#             # Manejar condicionales IF
#             elif isinstance(key, tuple) and key[0] == "if":
#                 if value:
#                     contenido_interno = procesar_bloque(value, nivel + 1, indice_base)
#                     terminos.append(f"C_if*({contenido_interno if contenido_interno else '1'})")
#                 else:
#                     terminos.append("C_if")
            
#             # Manejar ELSE
#             elif key == "else":
#                 if value:
#                     contenido_interno = procesar_bloque(value, nivel + 1, indice_base)
#                     terminos.append(f"C_else*({contenido_interno if contenido_interno else '1'})")
#                 else:
#                     terminos.append("C_else")
            
#             # Ignorar llamadas a funciones (no procesarlas por ahora)
#             elif key == "func_call":
#                 continue
        
#         # Combinar términos con suma
#         if terminos:
#             return " + ".join(terminos)
#         return ""
    
#     def procesar_funciones(lista_codigo: list) -> str:
#         """
#         Procesa la lista de funciones y genera sumatorias para cada una en formato SymPy
#         """
#         ecuaciones = []
        
#         for func_dict in lista_codigo:
#             for func_name, func_data in func_dict.items():
#                 variables = func_data.get("variables", [])
#                 code = func_data.get("code", {})
                
#                 # Obtener parámetros de entrada
#                 params = []
#                 for var in variables:
#                     if var[1]:  # Si tiene tamaño
#                         params.append(var[1].strip("[]"))
                
#                 param_str = ", ".join(params) if params else "n"
                
#                 # Procesar el código de la función
#                 sumatoria = procesar_bloque(code)
                
#                 if sumatoria:
#                     ecuaciones.append(f"T_{func_name}({param_str}) = {sumatoria}")
#                 else:
#                     ecuaciones.append(f"T_{func_name}({param_str}) = 1")
        
#         return "\n".join(ecuaciones)
    
#     resultado = procesar_funciones(codigo)
#     return resultado
from sympy import sympify
from sympy.abc import i, j, k, n
def convertir_a_sumatoria(codigo: list) -> str:
    """
    Convierte un codigo representado en forma de grafo/arbol a una sumatoria matematica usando SymPy
    """
    
    def procesar_bloque(bloque: dict, nivel: int = 0) -> str:
        """
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
                        terminos.append(f"Sum({contenido_interno}, ({indice_actual.name}, 1, {limite}))")
                    else:
                        terminos.append(f"Sum(1, ({indice_actual.name}, 1, {limite}))")
                else:
                    terminos.append(f"Sum(1, ({indice_actual.name}, 1, {limite}))")
            
            # Manejar ciclos WHILE
            elif isinstance(key, tuple) and key[0] == "while":
                condicion = key[1]
                if value:
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    terminos.append(f"W_{{{condicion}}}*({contenido_interno if contenido_interno else '1'})")
                else:
                    terminos.append(f"W_{{{condicion}}}")
            
            # Manejar condicionales IF
            elif isinstance(key, tuple) and key[0] == "if":
                if value:
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    terminos.append(f"({contenido_interno if contenido_interno else '1'})")
                else:
                    terminos.append("1")
            
            # Manejar ELSE
            elif key == "else":
                if value:
                    contenido_interno = procesar_bloque(value, nivel + 1)
                    terminos.append(f"({contenido_interno if contenido_interno else '1'})")
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
example = [
    {
        "func_name": {
            "variables": [("c", "[n]")],
            "code": {
                ("for", "n"): {},
                "func_call": (
                    "func_name",
                    [("c", "[n/2]"), ("a", "")],
                ),  # llamada recursiva con c dividido a la mitad
            },
        }
    },
    {
        "main": {
            "variables": [
                ("w", "[n]"),
            ],  # x es un array de 5 dimenciones. y es un array de 2x5, z es un escalar y w es un array de n dimensiones.
            "code": {
                ("for", "n"): {  # ciclo for que itera n veces
                    (
                        "for",
                        "n/2",
                    ): {  # ciclo for que itera k veces (donde k  es una variable dependiente de n)
                        (
                            "if",
                            "condicion"
                        ): {},  # if con condicion booleana que ejecuta un bloque de costo c
                        "else": {
                            ("while", "condicion"): {},
                        },  # condicion del while depende de la entrada de datos
                        "func_call": (
                            "func_name",
                            [("w", "[n]"), ("a", "")],
                        ),  # llamada a funcion, entra la variable w y a que es una variable escalar/normal
                    },
                },
            },
        },
    },
]

print(convertir_a_sumatoria(example))