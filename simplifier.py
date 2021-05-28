from calculator import calculate
from math_ast import *

def is_var_dependant(tree: MathAST) -> bool:
    if isinstance(tree, DoubleToken):
        a = is_var_dependant(tree.a)
        b = is_var_dependant(tree.b)
        return a or b
    elif isinstance(tree, SingleToken): 
        return is_var_dependant(tree.a)
    elif isinstance(tree, Variable): 
        return True
    else: 
        return False

def simplify(ast: MathAST) -> MathAST:
    if isinstance(ast, LeafToken):
        return ast
    
    if not is_var_dependant(ast):
        return Constant(calculate(ast))

    if isinstance(ast, SingleToken):
        ast.a = simplify(ast.a)
        return ast
    elif isinstance(ast, DoubleToken):
        ast.a = simplify(ast.a)
        ast.b = simplify(ast.b)
        if isinstance(ast, Add):
            if isinstance(ast.a, Constant) and (ast.a.value == 0):
                return ast.b
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
    return ast