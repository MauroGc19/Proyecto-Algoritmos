from  lark import Lark, Transformer, v_args
lark_file = "docs/lark.txt"
pseudo_grammar = ""
with open(lark_file, 'r', encoding='utf-8') as f:
    pseudo_grammar = f.read()
def pedir_dato(nombre, tipo="var", dimensiones=None):
    if tipo == "arreglo":
        if dimensiones is None or len(dimensiones) == 0:
            n = int(input(f"Ingrese la cantidad de elementos para el arreglo {nombre}: "))
            return [input(f"{nombre}[{i}]=") for i in range(n)]
        else:
            # Soporte para arreglos multidimensionales
            dim = dimensiones[0]
            if isinstance(dim, str) and dim.isdigit():
                dim = int(dim)
            elif isinstance(dim, int):
                pass
            else:
                dim = int(input(f"Ingrese la cantidad de elementos para la dimensión de {nombre}: "))
            return [pedir_dato(f"{nombre}[{i}]", "arreglo", dimensiones[1:]) for i in range(dim)]
    else:
        return input(f"Ingrese el valor para {nombre}: ")


class PseudoTransformer(Transformer):
    def __init__(self):
        self.variables = {}
        self.arreglos = {}
        self.clases = {}
        self.objetos = {}
        self.subrutinas = {}
        self.errores = []
        self.asignacion_en_linea = False

    def assignment(self, items):
        if self.asignacion_en_linea:
            self.errores.append("Error: No se permiten asignaciones múltiples en una sola línea.")
        self.asignacion_en_linea = True
        var = str(items[0])
        val = items[1]
        # Asignación por referencia para arreglos/objetos
        if isinstance(val, dict) or isinstance(val, list):
            self.variables[var] = val
        elif isinstance(val, str) and val in self.variables and (isinstance(self.variables[val], dict) or isinstance(self.variables[val], list)):
            self.variables[var] = self.variables[val]
        else:
            self.variables[var] = val

    def input_stmt(self, items):
        var = str(items[0])
        # Si la variable es un arreglo declarado
        if var in self.arreglos:
            dimensiones = self.arreglos[var]
            val = pedir_dato(var, "arreglo", dimensiones)
        else:
            val = pedir_dato(var)
        self.variables[var] = val

    def var_name(self, items):
        return str(items[0])

    def NUMBER(self, n):
        return int(n)

    def string(self, items):
        return str(items[0])[1:-1]

    def graph_expr(self, items):
        return str(items[0])

    def expr_factor(self, items):
        return items[0]

    def expr_arith(self, items):
        if len(items) == 1:
            return items[0]
        return items

    def expr_cmp(self, items):
        return items

    def expr_bool(self, items):
        return items

    def expr_and(self, items):
        return items

    def expr_not(self, items):
        return items

    def for_loop(self, items):
        pass

    def while_loop(self, items):
        pass

    def repeat_loop(self, items):
        pass

    def if_statement(self, items):
        pass

    def class_def(self, items):
        nombre = str(items[0])
        atributos = [str(a) for a in items[1:]]
        self.clases[nombre] = atributos

    def object_decl(self, items):
        clase = str(items[0])
        nombre = str(items[1])
        self.objetos[nombre] = clase

    def subroutine_def(self, items):
        nombre = str(items[0])
        parametros = items[1] if len(items) > 2 else []
        cuerpo = items[-1]
        self.subrutinas[nombre] = {"parametros": parametros, "cuerpo": cuerpo}

    def function_decl(self, items):
        nombre = str(items[0])
        parametros = items[1] if len(items) > 1 else []
        cuerpo = items[-1]
        self.subrutinas[nombre] = {"parametros": parametros, "cuerpo": cuerpo}

        # Solicitar valores para los parámetros
        print(f"Definiendo función: {nombre}")
        valores_parametros = {}
        for param in parametros:
            valor = input(f"Ingrese el valor para el parámetro '{param}': ")
            valores_parametros[param] = valor
        self.variables.update(valores_parametros)

    def param_list(self, items):
        return items

    def param(self, items):
        # Identificar si el parámetro es un arreglo (tiene '[]')
        nombre_param = str(items[0])
        if nombre_param.endswith("[]"):
            return ("arreglo", nombre_param[:-2])  # Retorna el nombre sin '[]' y lo marca como arreglo
        return nombre_param  # Retorna el nombre del parámetro como cadena normal

    def array_param(self, items):
        return ("arreglo", str(items[0]), items[1])

    def array_dims(self, items):
        return items

    def object_param(self, items):
        return ("objeto", str(items[0]), str(items[1]))

    def subroutine_call(self, items):
        nombre = str(items[0])
        argumentos = items[1] if len(items) > 1 else []
        if nombre not in self.subrutinas:
            self.errores.append(f"Error: Subrutina '{nombre}' no definida.")
        # Validación de cantidad de parámetros
        else:
            params = self.subrutinas[nombre]["parametros"]
            if len(argumentos) != len(params):
                self.errores.append(f"Error: Número de parámetros incorrecto en llamada a '{nombre}'.")

    def arg_list(self, items):
        return items

    def arr_access(self, items):
        nombre = str(items[0])
        indices = items[1:]
        # Registrar dimensiones si no existen
        if nombre not in self.arreglos:
            self.arreglos[nombre] = [None]*len(indices)
        return ("arreglo", nombre, indices)
    def array_param(self, items):
        nombre = str(items[0])
        dimensiones = items[1]
        self.arreglos[nombre] = dimensiones
        return ("arreglo", nombre, dimensiones)

    def func_call(self, items):
        # length(A)
        return ("length", str(items[0]))

    def COMMENT(self, _):
        pass

    def start(self, items):
        self.asignacion_en_linea = False
        return items

# Función principal para compilar un archivo txt

def compilar_archivo_txt(ruta):
    with open(ruta, encoding='utf-8') as f:
        codigo = f.read()
    
    # Parser sin transformer para obtener el árbol
    parser = Lark(pseudo_grammar, parser="lalr")
    tree = parser.parse(codigo)
    
    # Imprimir el árbol en formato pretty
    print(tree.pretty())
    
    return tree

# Función para visualizar el árbol de parsing
def visualizar_arbol(ruta):
    with open(ruta, encoding='utf-8') as f:
        codigo = f.read()
    
    # Parser sin transformer para obtener el árbol
    parser = Lark(pseudo_grammar, parser="lalr")
    tree = parser.parse(codigo)
    
    # Imprimir el árbol en formato pretty
    print(tree.pretty())
    
    return tree

# Función para analizar llamados recursivos y ciclos
def analizar_llamados_recursivos(tree, nombre_funcion_actual=None):
    """
    Analiza el árbol para encontrar llamados recursivos
    """
    llamados = []
    
    def buscar_llamados(node, funcion_actual):
        if hasattr(node, 'data'):
            # Detectar definición de subrutina/función
            if node.data == 'subroutine_def' or node.data == 'function_decl':
                nombre = str(node.children[0])
                funcion_actual = nombre
                print(f"\n📦 Función/Subrutina definida: {nombre}")
            
            # Detectar llamados a subrutinas
            elif node.data == 'subroutine_call':
                nombre_llamado = str(node.children[0])
                if funcion_actual:
                    print(f"  ↳ Llamado a: {nombre_llamado}")
                    if nombre_llamado == funcion_actual:
                        print(f"    ⚠️  RECURSIÓN DETECTADA en {funcion_actual}")
                        llamados.append(('recursivo', funcion_actual, nombre_llamado))
                    else:
                        llamados.append(('llamado', funcion_actual, nombre_llamado))
            
            # Detectar ciclos
            elif node.data in ['for_loop', 'while_loop', 'repeat_loop']:
                tipo_ciclo = node.data.replace('_', ' ').upper()
                print(f"  🔁 {tipo_ciclo} detectado")
            
            # Recursión en hijos
            for child in node.children:
                buscar_llamados(child, funcion_actual)
    
    buscar_llamados(tree, nombre_funcion_actual)
    return llamados

# Función para generar un grafo de llamados (usando graphviz si está instalado)
def generar_grafo_llamados(tree):
    """
    Genera un grafo de llamados de funciones
    Requiere: pip install graphviz
    """
    try:
        from graphviz import Digraph
        
        dot = Digraph(comment='Grafo de Llamados')
        dot.attr(rankdir='TB')
        
        funciones = set()
        llamados = []
        
        def extraer_info(node, funcion_actual=None):
            if hasattr(node, 'data'):
                if node.data in ['subroutine_def', 'function_decl']:
                    nombre = str(node.children[0])
                    funciones.add(nombre)
                    funcion_actual = nombre
                elif node.data == 'subroutine_call' and funcion_actual:
                    nombre_llamado = str(node.children[0])
                    llamados.append((funcion_actual, nombre_llamado))
                
                for child in node.children:
                    extraer_info(child, funcion_actual)
        
        extraer_info(tree)
        
        # Agregar nodos
        for func in funciones:
            dot.node(func, func, shape='box')
        
        # Agregar aristas
        for origen, destino in llamados:
            if origen == destino:
                dot.edge(origen, destino, label='recursivo', color='red', style='bold')
            else:
                dot.edge(origen, destino)
        
        # Guardar y renderizar
        dot.render('call_graph', format='png', cleanup=True)
        print("\n✅ Grafo generado: call_graph.png")
        
    except ImportError:
        print("\n⚠️  Para generar gráficos instale: pip install graphviz")

if __name__ == "__main__":
    archivo = "test/txt/binary_search.ayd"
    
    print("=" * 60)
    print("ÁRBOL DE SINTAXIS")
    print("=" * 60)
    tree = visualizar_arbol(archivo)
    
    print("\n" + "=" * 60)
    print("ANÁLISIS DE LLAMADOS Y RECURSIÓN")
    print("=" * 60)
    analizar_llamados_recursivos(tree)
    
    print("\n" + "=" * 60)
    print("GENERANDO GRAFO DE LLAMADOS")
    print("=" * 60)
    generar_grafo_llamados(tree)
    
    print("\n" + "=" * 60)
    print("COMPILACIÓN NORMAL")
    print("=" * 60)
    compilar_archivo_txt(archivo)
