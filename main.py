from calculator import calculate
from simplifier import simplify
from derivative import differentiate, detect_vars_and_diff
from math_ast import *
from math_parser import parse 
from math_composer import compose

f = input('function:\n> ')
try:
    ast = parse(f)
    ast = simplify(ast)
    print('simplified:\n'+compose(ast))
    deriv_ast = detect_vars_and_diff(ast)
    print('derivative:\n'+compose(deriv_ast))
    deriv_ast = simplify(deriv_ast)
    print('simplified derivative:\n'+compose(deriv_ast))
except Exception as e:
    print(e)