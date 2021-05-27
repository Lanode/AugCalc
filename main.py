from derivative import differentiate
from math_ast import *
from math_parser import parse 
from composer import compose

#f = Div(Constant(1), Mul(Constant(2), Pow(Variable("x"), Constant(2))))
# f = Cos(Usub(Variable("x")))
# x = derivative.differentiate(f, "x")
# print()

f = input('fun: ')
v = input('var: ')
ast = parse(f)
deriv_ast = differentiate(ast, v)
print('derivative: '+compose(deriv_ast))