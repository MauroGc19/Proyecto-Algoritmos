# analizador_lexico.py
"""
Analizador léxico para el compilador de pseudocódigo.
Reglas implementadas:
1. El símbolo “►” indica que el resto de la línea es un comentario.
2. La asignación se indica mediante el símbolo “🡨”.
3. No se permiten asignaciones múltiples.
18. Los parámetros son pasados a los procedimientos por valor. El procedimiento llamado recibe su propia copia de los parámetros, y si él asigna un valor a un parámetro el cambio no es visto por el procedimiento que llama. Cuando los objetos son pasados, el apuntador a los datos representando al objeto es copiado, pero los campos del objeto no. Por ejemplo, si x es un parámetro de un procedimiento llamado, la asignación  y 🡨 x  dentro del procedimiento llamado no es visible al procedimiento que llama. La asignación  x.f 🡨 3, sin embargo, sí es visible.
19. La definición de los parámetros en una subrutina se hace de la siguiente forma:
    nombre_subrutina(parámetro1, parámetro2, ..., parámetrok)
        begin
            accion1
            ...
        end
    Si un parámetro es un arreglo: nombre_arreglo[n]..[m] (los valores dentro de los corchetes son opcionales, y se usan tantos corchetes como dimensiones tenga el arreglo).
    Si un parámetro es un objeto: Clase nombre_objeto.
    Cualquier otro parámetro: solo el nombre.
    El llamado a una subrutina se hace con CALL seguido por el nombre de la subrutina y entre paréntesis, el nombre de los parámetros.
"""

import re


class AnalizadorLexico:
    """
    Analizador léxico para el compilador de pseudocódigo.
    Reglas implementadas:
    1. El símbolo “►” indica que el resto de la línea es un comentario.
    2. La asignación se indica mediante el símbolo “🡨”.
    3. No se permiten asignaciones múltiples.
    7. length(A) para obtener el tamaño de un arreglo.
    8. Estructura para manejo de cadenas.
    9. Estructura para manejo de grafos.
    12. Operadores booleanos: and, or, not (short-circuiting).
    13. Valores booleanos: T (true), F (false).
    14. Operadores relacionales: <, >, <=, >=, =, <>, ≠.
    15. Operadores matemáticos: +, -, *, /, mod, div, techo (┌ ┐), piso (└ ┘).
    16. Asignación por referencia: una variable que representa un arreglo u objeto es tratada como un puntero. Si y 🡨 x, entonces x y y apuntan al mismo objeto/arreglo.
    17. Un puntero puede tener el valor especial NULL si no refiere a ningún objeto.
    18. Los parámetros son pasados a los procedimientos por valor. El procedimiento llamado recibe su propia copia de los parámetros, y si él asigna un valor a un parámetro el cambio no es visto por el procedimiento que llama. Cuando los objetos son pasados, el apuntador a los datos representando al objeto es copiado, pero los campos del objeto no. Por ejemplo, si x es un parámetro de un procedimiento llamado, la asignación  y 🡨 x  dentro del procedimiento llamado no es visible al procedimiento que llama. La asignación  x.f 🡨 3, sin embargo, sí es visible.
    """

    def __init__(self, codigo):
        self.codigo = codigo
        self.tokens = []

    def eliminar_comentarios(self):
        lineas = self.codigo.split("\n")
        sin_comentarios = []
        for linea in lineas:
            if "►" in linea:
                linea = linea.split("►")[0]
            sin_comentarios.append(linea)
        self.codigo = "\n".join(sin_comentarios)

    def obtener_tokens(self):
        self.eliminar_comentarios()
        # Patron extendido para arreglos, length, cadenas, grafos, operadores y booleanos
        patron = r"""
            (length\s*\([a-zA-Z_][a-zA-Z0-9_]*\))
            |(\bmod\b|\bdiv\b|\band\b|\bor\b|\bnot\b|\bT\b|\bF\b)
            |([a-zA-Z_][a-zA-Z0-9_]*)
            |(🡨)
            |([0-9]+)
            |([+\-*/=()\[\]\.\.<>≤≥≠])
            |(<=|>=|<>|≠)
            |([\u2308\u230A\u2309\u230B])
            |('(?:[^'\\]|\\.)*')
            |(\"(?:[^\"\\]|\\.)*\")
        """
        patron = patron.replace("\n", "").replace("    ", "")
        for linea in self.codigo.split("\n"):
            tokens_linea = re.findall(patron, linea)
            # Unir todos los grupos en un solo token por coincidencia
            tokens_linea = [next(filter(None, t)) for t in tokens_linea if any(t)]
            self.tokens.append(tokens_linea)
        return self.tokens

    # Comentario: para la regla 8 (cadenas), se reconocen tokens entre comillas simples o dobles.
    # Para la regla 9 (grafos), se recomienda definir palabras clave como 'grafo', 'nodo', 'arista', etc.,
    # y agregarlas a la gramática del analizador sintáctico.
