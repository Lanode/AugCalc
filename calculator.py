from math_ast import *
import math

def calculate(ast: MathAST) -> float:
    if isinstance(ast, Constant):
        return ast.value
    elif isinstance(ast, Pi):
        return math.pi
    elif isinstance(ast, Exponenta):
        return math.e
    elif isinstance(ast, Sin):
        return math.sin(calculate(ast.a))
    elif isinstance(ast, Cos):
        return math.cos(calculate(ast.a))
    elif isinstance(ast, Tg):
        return math.tg(calculate(ast.a))
    elif isinstance(ast, Ctg):
        return math.cos(calculate(ast.a))/math.sin(calculate(ast.a))
    elif isinstance(ast, Ln):
        return math.log10(calculate(ast.a))
    elif isinstance(ast, Usub):
        return -calculate(ast.a)
    elif isinstance(ast, Arcsin):
        return math.asin(calculate(ast.a))
    elif isinstance(ast, Arccos):
        return math.acos(calculate(ast.a))
    elif isinstance(ast, Arctg):
        return math.atan(1/calculate(ast.a))
    elif isinstance(ast, Sqrt):
        return math.sqrt(calculate(ast.a))

    elif isinstance(ast, Add):
        return calculate(ast.a) + calculate(ast.b)
    elif isinstance(ast, Sub):
        return calculate(ast.a) - calculate(ast.b)
    elif isinstance(ast, Mul):
        return calculate(ast.a) * calculate(ast.b)
    elif isinstance(ast, Div):
        return calculate(ast.a) / calculate(ast.b)
    elif isinstance(ast, Pow):
        return calculate(ast.a) ^ calculate(ast.b)
    
    else:
        raise Exception('Calculate error: unknown MathAST node type')