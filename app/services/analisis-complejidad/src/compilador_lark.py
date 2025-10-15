from  lark import Lark, Transformer, v_args
pseudo_grammar = r'''
    start: statement+

    statement: assignment
             | for_loop
             | while_loop
             | repeat_loop
             | if_statement
             | class_def
             | object_decl
             | subroutine_def
             | subroutine_call
             | COMMENT
             | input_stmt
             | function_decl

    assignment: var_name "🡨" expr
    input_stmt: "leer" var_name

    for_loop: "for" var_name expr "to" expr "do" "begin" statement+ "end"
    while_loop: "while" "(" expr ")" "do" "begin" statement+ "end"
    repeat_loop: "repeat" statement+ "until" "(" expr ")"
    if_statement: "if" "(" expr ")" "then" "begin" statement+ "end" ("else" "begin" statement+ "end")?

    class_def: CNAME "{" attr_list "}"
    attr_list: var_name+
    object_decl: CNAME var_name

    subroutine_def: CNAME "(" param_list? ")" "begin" statement+ "end"
    param_list: param ("," param)*
    param: array_param | object_param | var_name
    array_param: var_name array_dims
    array_dims: ("[" (NUMBER | var_name)? "]")+
    object_param: CNAME var_name

    subroutine_call: "CALL" CNAME "(" arg_list? ")"
    arg_list: expr ("," expr)*

    function_decl: "FUNCION" CNAME "(" param_list? ")" "begin" statement+ "end"

    expr: expr_bool
    expr_bool: expr_bool "or" expr_and   -> or_op
             | expr_and
    expr_and: expr_and "and" expr_not    -> and_op
             | expr_not
    expr_not: "not" expr_cmp             -> not_op
             | expr_cmp
    expr_cmp: expr_arith rel_op expr_arith -> rel_op
             | expr_arith
    rel_op: "<" | ">" | "<=" | ">=" | "=" | "<>" | "≠"
    expr_arith: expr_arith add_op expr_term -> arith_op
              | expr_term
    add_op: "+" | "-"
    expr_term: expr_term mul_op expr_factor -> arith_op
             | expr_factor
    mul_op: "*" | "/" | "mod" | "div"
    expr_factor: var_name
               | NUMBER
               | "T" | "F"
               | "NULL"
               | "(" expr ")"
               | arr_access
               | func_call
               | string
               | graph_expr
    arr_access: var_name ("[" expr "]")+ 
    func_call: "length" "(" var_name ")"
    string: /'(?:[^'\\]|\\.)*'/ | /"(?:[^"\\]|\\.)*"/
    graph_expr: "grafo" | "nodo" | "arista"
    var_name: CNAME
    COMMENT: /►.*/
    NUMBER: /[0-9]+/
    %import common.CNAME
    %import common.WS
    %ignore WS
'''
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
    parser = Lark(pseudo_grammar, parser="lalr", transformer=PseudoTransformer())
    parser.parse(codigo)
    print("El archivo se compiló correctamente.")

if __name__ == "__main__":
    archivo = "app/services/analisis-complejidad/test/Prueba1.txt"
    compilar_archivo_txt(archivo)
