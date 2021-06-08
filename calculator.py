from math_parser import parse
from math_ast import *
import math

def calculate(ast: MathAST, **kwargs) -> float:
    def calc(ast: MathAST) -> float:
        if isinstance(ast, Constant):
            return ast.value
        elif isinstance(ast, Pi):
            return math.pi
        elif isinstance(ast, Exponenta):
            return math.e
        elif isinstance(ast, Sin):
            return math.sin(calc(ast.a))
        elif isinstance(ast, Cos):
            return math.cos(calc(ast.a))
        elif isinstance(ast, Tg):
            return math.tan(calc(ast.a))
        elif isinstance(ast, Ctg):
            return math.cos(calc(ast.a))/math.sin(calc(ast.a))
        elif isinstance(ast, Ln):
            return math.log10(calc(ast.a))
        elif isinstance(ast, Usub):
            return -calc(ast.a)
        elif isinstance(ast, Arcsin):
            return math.asin(calc(ast.a))
        elif isinstance(ast, Arccos):
            return math.acos(calc(ast.a))
        elif isinstance(ast, Arctg):
            return math.atan(1/calc(ast.a))
        elif isinstance(ast, Sqrt):
            return math.sqrt(calc(ast.a))

        elif isinstance(ast, Add):
            return calc(ast.a) + calc(ast.b)
        elif isinstance(ast, Sub):
            return calc(ast.a) - calc(ast.b)
        elif isinstance(ast, Mul):
            return calc(ast.a) * calc(ast.b)
        elif isinstance(ast, Div):
            return calc(ast.a) / calc(ast.b)
        elif isinstance(ast, Pow):
            return calc(ast.a) ** calc(ast.b)
        
        elif isinstance(ast, Variable):
            if ast.name in kwargs:
                return kwargs[ast.name]
            else:
                raise Exception('Calculate error: no value provided for variable: '+ast.name)

        else:
            raise Exception('Calculate error: unknown MathAST node type')
    return calc(ast)

if __name__ == "__main__":
    print(calculate(parse('(4+6/5)-3.5'), x=4, a=3.5))