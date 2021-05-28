from simplifier import simplify
from derivative import differentiate
from math_ast import *
from math_parser import parse 
from math_composer import compose

#f = Div(Constant(1), Mul(Constant(2), Pow(Variable("x"), Constant(2))))
# f = Cos(Usub(Variable("x")))
# x = derivative.differentiate(f, "x")
# print()

f = input('fun: ')
v = input('var: ')
ast = parse(f)
#ast = simplify(ast)
deriv_ast = differentiate(ast, v)
print(compose(deriv_ast))
deriv_ast = simplify(deriv_ast)
print(compose(deriv_ast))
print('derivative: '+compose(deriv_ast))