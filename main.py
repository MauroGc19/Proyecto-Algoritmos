import sympy

cadena = "Sum(Sum(1, (k, 1, m)), (k, 1, m))"

expr = sympy.sympify(cadena)
print(expr)
print(expr.doit())