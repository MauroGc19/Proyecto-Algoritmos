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
                        "k",
                    ): {  # ciclo for que itera k veces (donde k  es una variable dependiente de n)
                        (
                            "if",
                            "condicion",
                            0.7,  # probabilidad estimada
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


### La idea es simplificar el codigo lo maximo possible para poder calcular las eficiencias
### Utilizando una representacion en forma de grafo o arbol
### Luego, a partir de esa representacion, calcular las eficiencias

### primero se define las variables. unicamente se consideran arrays y matrices que dependean de una entrada de datos
### despues empezamos a construir el grafo a partir del codigo.
### se consideran ciclos for, ciclos while, condicionales y llamadas a funciones
### unicamente representamos cosas que dependan de la entrada de datos o puedan afectar la ejecucion del programa
### fors con valores constantes no seran considerados
### condiciones que no afectan mucho (que su ejecucion interna es constante) no seran consideradas
