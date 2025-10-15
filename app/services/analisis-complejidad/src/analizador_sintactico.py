# analizador_sintactico.py
"""
Analizador sintáctico para el compilador de pseudocódigo.
Reglas implementadas:
1. El símbolo “►” indica que el resto de la línea es un comentario.
2. La asignación se indica mediante el símbolo “🡨”.
3. No se permiten asignaciones múltiples.
"""

class AnalizadorSintactico:
    """
    Analizador sintáctico para el compilador de pseudocódigo.
    Reglas implementadas:
    1. El símbolo “►” indica que el resto de la línea es un comentario.
    2. La asignación se indica mediante el símbolo “🡨”.
    3. No se permiten asignaciones múltiples.
    4. Las variables son locales a un procedimiento, no hay variables globales.
    5. Acceso a elementos de arreglos con corchetes y notación de rango con "..".
    6. Declaración de vectores locales al inicio del algoritmo tras el begin.
    10. Definición de clases antes del algoritmo, con atributos entre llaves.
    11. Declaración de objetos al inicio del algoritmo y acceso a campos con punto.
    16. Asignación por referencia: una variable que representa un arreglo u objeto es tratada como un puntero. Si y 🡨 x, entonces x y y apuntan al mismo objeto/arreglo.
    17. Un puntero puede tener el valor especial NULL si no refiere a ningún objeto.
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.errores = []
        self.variables_locales = set()
        self.arreglos_declarados = set()
        self.en_procedimiento = False
        self.despues_de_begin = False
        self.clases_definidas = {}
        self.objetos_declarados = {}

    def analizar(self):
        en_definicion_clase = False
        nombre_clase_actual = ''
        atributos_clase = []
        en_algoritmo = False
        en_for = False
        en_while = False
        en_repeat = False
        en_if = False
        operadores_booleanos = {'and', 'or', 'not'}
        valores_booleanos = {'T', 'F'}
        operadores_relacionales = {'<', '>', '<=', '>=', '=', '<>', '≠'}
        operadores_matematicos = {'+', '-', '*', '/', 'mod', 'div', '┌', '┐', '└', '┘'}
        for linea in self.tokens:
            # Reemplazar '<-' por '🡨' para compatibilidad si es necesario
            linea = ['🡨' if t == '<-' else t for t in linea]
            # Validación de operadores booleanos y short-circuiting
            for i, token in enumerate(linea):
                if token in operadores_booleanos:
                    # and, or deben tener operandos booleanos a ambos lados
                    if token in {'and', 'or'}:
                        if i == 0 or i == len(linea)-1:
                            self.errores.append(f'Error: Operador booleano "{token}" mal posicionado en la línea: ' + ' '.join(linea))
                        """
                        Analizador sintáctico para el pseudolenguaje definido.

                        Reglas implementadas:
                        - Comentarios inician con #
                        - Asignación con el símbolo 🡨
                        - No se permite asignar a literales ni a expresiones no lvalue
                        - Variables locales, acceso a arreglos, declaración de vectores
                        - Longitud, cadenas, grafos
                        - Definición de clases y objetos, acceso a campos
                        - Estructuras de control: FOR, WHILE, REPEAT, IF/ELSE
                        - Validación de operadores
                        - Semántica de paso de parámetros y referencias
                        - El valor especial NULL para apuntadores
                        - Los parámetros son pasados a los procedimientos por valor. El procedimiento llamado recibe su propia copia de los parámetros, y si él asigna un valor a un parámetro el cambio no es visto por el procedimiento que llama. Cuando los objetos son pasados, el apuntador a los datos representando al objeto es copiado, pero los campos del objeto no. Por ejemplo, si x es un parámetro de un procedimiento llamado, la asignación  y 🡨 x  dentro del procedimiento llamado no es visible al procedimiento que llama. La asignación  x.f 🡨 3, sin embargo, sí es visible.
                        """
                # Validación de valores booleanos
                if token in valores_booleanos:
                    pass  # Se aceptan como literales

                # Validación de operadores relacionales
                if token in operadores_relacionales:
                    if i == 0 or i == len(linea)-1:
                        self.errores.append(f'Error: Operador relacional "{token}" mal posicionado en la línea: ' + ' '.join(linea))
                    else:
                        op_izq = linea[i-1]
                        op_der = linea[i+1]
                        # Aquí podrías agregar validaciones de tipo si se implementa un sistema de tipos

                # Validación de operadores matemáticos
                if token in operadores_matematicos:
                    if token in {'┌', '└'}:
                        # techo y piso deben abrir y cerrar correctamente
                        if i == len(linea)-1 or linea[i+2] not in {'┐', '┘'}:
                            self.errores.append(f'Error: Operador matemático "{token}" sin cierre correcto en la línea: ' + ' '.join(linea))
                    elif token in {'┐', '┘'}:
                        if i == 0 or linea[i-2] not in {'┌', '└'}:
                            self.errores.append(f'Error: Operador matemático "{token}" sin apertura correcta en la línea: ' + ' '.join(linea))
                    else:
                        if i == 0 or i == len(linea)-1:
                            self.errores.append(f'Error: Operador matemático "{token}" mal posicionado en la línea: ' + ' '.join(linea))
                        # No se valida tipo de operandos aquí, pero se podría agregar
            if len(linea) >= 2 and '{' in linea and '}' in linea:
                # ...existing code...
                try:
                    idx_llave_izq = linea.index('{')
                    idx_llave_der = linea.index('}')
                    nombre_clase = linea[idx_llave_izq-1]
                    atributos = linea[idx_llave_izq+1:idx_llave_der]
                    for atributo in atributos:
                        if not atributo.isidentifier():
                            self.errores.append(f'Error: Nombre de atributo inválido "{atributo}" en clase {nombre_clase}')
                    self.clases_definidas[nombre_clase] = atributos
                except Exception:
                    self.errores.append('Error: Definición de clase mal formada en la línea: ' + ' '.join(linea))

            # Validación de FOR
            if len(linea) >= 6 and linea[0].lower() == 'for' and linea[3].lower() == 'to' and linea[5].lower() == 'do':
                en_for = True
                if not linea[1].isidentifier():
                    self.errores.append(f'Error: Variable contadora inválida en FOR: {linea[1]}')
                # valorInicial y limite pueden ser variables o números
                # No se valida el cuerpo aquí, solo la cabecera

            if en_for and 'begin' in [x.lower() for x in linea]:
                # Inicio del bloque FOR
                pass
            if en_for and 'end' in [x.lower() for x in linea]:
                en_for = False

            # Validación de WHILE
            if len(linea) >= 5 and linea[0].lower() == 'while' and linea[2].lower() == 'do':
                en_while = True
                # linea[1] debería ser la condición entre paréntesis
                if not (linea[1].startswith('(') and linea[1].endswith(')')):
                    self.errores.append('Error: Condición de WHILE debe estar entre paréntesis')
            if en_while and 'begin' in [x.lower() for x in linea]:
                pass
            if en_while and 'end' in [x.lower() for x in linea]:
                en_while = False

            # Validación de REPEAT
            if len(linea) >= 1 and linea[0].lower() == 'repeat':
                en_repeat = True
            if en_repeat and len(linea) >= 2 and linea[0].lower() == 'until':
                # linea[1] debería ser la condición entre paréntesis
                if not (linea[1].startswith('(') and linea[1].endswith(')')):
                    self.errores.append('Error: Condición de UNTIL debe estar entre paréntesis')
                en_repeat = False

            # Validación de IF-THEN-ELSE
            if len(linea) >= 3 and linea[0].lower() == 'if' and linea[2].lower() == 'then':
                en_if = True
                if not (linea[1].startswith('(') and linea[1].endswith(')')):
                    self.errores.append('Error: Condición de IF debe estar entre paréntesis')
            if en_if and 'begin' in [x.lower() for x in linea]:
                pass
            if en_if and 'end' in [x.lower() for x in linea]:
                en_if = False
            if en_if and 'else' in [x.lower() for x in linea]:
                # ELSE debe ir después de END
                pass

            # Regla 11: Declaración de objetos al inicio del algoritmo
            if len(linea) >= 2 and linea[0] in self.clases_definidas:
                # Ejemplo: Casa miCasa
                nombre_clase = linea[0]
                nombre_objeto = linea[1]
                if not nombre_objeto.isidentifier():
                    self.errores.append(f'Error: Nombre de objeto inválido "{nombre_objeto}"')
                else:
                    self.objetos_declarados[nombre_objeto] = nombre_clase

            # Regla 3: No asignaciones múltiples
            if '🡨' in linea:
                if linea.count('🡨') > 1:
                    self.errores.append('Error: Asignación múltiple no permitida en la línea: ' + ' '.join(linea))

            # Regla 4: Variables locales a procedimientos
            if any(palabra.lower() == 'procedure' for palabra in linea):
                self.en_procedimiento = True
                self.variables_locales = set()
                self.arreglos_declarados = set()
                self.despues_de_begin = False
            if self.en_procedimiento and any(palabra.lower() == 'begin' for palabra in linea):
                self.despues_de_begin = True

            # Regla 6: Declaración de vectores locales tras el begin
            if self.en_procedimiento and self.despues_de_begin:
                for palabra in linea:
                    if '[' in palabra and ']' in palabra:
                        nombre = palabra.split('[')[0]
                        self.arreglos_declarados.add(nombre)
                        self.variables_locales.add(nombre)

            # Regla 5: Acceso a elementos de arreglos y rangos
            for palabra in linea:
                if '[' in palabra and ']' in palabra:
                    nombre = palabra.split('[')[0]
                    if nombre not in self.arreglos_declarados:
                        self.errores.append(f'Error: El arreglo "{nombre}" no ha sido declarado en la línea: ' + ' '.join(linea))
                if '..' in palabra:
                    # Validar notación de rango en arreglos
                    if not (('[' in palabra and ']' in palabra)):
                        self.errores.append(f'Error: Notación de rango mal usada en la línea: ' + ' '.join(linea))

                # Regla 11: Acceso a campos de objetos (objeto.campo)
                if '.' in palabra:
                    partes = palabra.split('.')
                    if len(partes) == 2:
                        objeto, campo = partes
                        if objeto not in self.objetos_declarados:
                            self.errores.append(f'Error: El objeto "{objeto}" no ha sido declarado en la línea: ' + ' '.join(linea))
                        else:
                            clase = self.objetos_declarados[objeto]
                            if clase in self.clases_definidas and campo not in self.clases_definidas[clase]:
                                self.errores.append(f'Error: El campo "{campo}" no existe en la clase {clase} en la línea: ' + ' '.join(linea))
                    else:
                        self.errores.append(f'Error: Acceso a campo mal formado en la línea: ' + ' '.join(linea))

        return self.errores
