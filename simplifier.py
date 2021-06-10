from math import pi
from calculator import calculate
from math_ast import *
from utils import *

def simplify(ast: MathAST) -> MathAST:
    if isinstance(ast, LeafToken):
        return ast
    
    if not is_var_dependant(ast):
        return Constant(calculate(ast))

    if isinstance(ast, SingleToken):
        ast.a = simplify(ast.a)
        if isinstance(ast, Usub) and isinstance(ast.a, Usub):
            return ast.a.a
    elif isinstance(ast, DoubleToken):
        ast.a = simplify(ast.a)
        ast.b = simplify(ast.b)
        # if not is_var_dependant(ast):
        #     return Constant(calculate(ast))
        if isinstance(ast, Add):
            if isinstance(ast.a, Constant) and (ast.a.value == 0):
                return ast.b
            elif isinstance(ast.b, Constant) and (ast.b.value == 0):
                return ast.a
        elif isinstance(ast, Sub):
            if isinstance(ast.a, Constant) and (ast.a.value == 0):
                return Usub(ast.b)
            elif isinstance(ast.b, Constant) and (ast.b.value == 0):
                return ast.a
        elif isinstance(ast, Mul):
            if (isinstance(ast.a, Constant) and (ast.a.value == 0)) \
               or (isinstance(ast.b, Constant) and (ast.b.value == 0)):
                return Constant(0)
            elif isinstance(ast.a, Constant) and (ast.a.value == 1):
                return ast.b
            elif isinstance(ast.b, Constant) and (ast.b.value == 1):
                return ast.a
        elif isinstance(ast, Div):
            if isinstance(ast.a, Constant) and (ast.a.value == 0):
                return Constant(0)
            elif isinstance(ast.b, Constant) and (ast.b.value == 1):
                return ast.a
        elif isinstance(ast, Pow):
            if isinstance(ast.b, Constant) and (ast.b.value == 0):
                return Constant(1)
            elif isinstance(ast.b, Constant) and (ast.b.value == 1):
                return ast.a
    return ast