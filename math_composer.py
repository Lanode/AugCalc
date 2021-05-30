from math_ast import *

def compose(ast: MathAST) -> str:
    def wrap_parethesis(t: MathAST) -> str:
        if isinstance(t, LeafToken) or isinstance(t, SingleToken):
            return compose(t)
        else:
            return '(' + compose(t) + ')'

    if isinstance(ast, Pi):
        return 'pi'
    elif isinstance(ast, Exponenta):
        return 'e'
    elif isinstance(ast, SingleToken):
        if isinstance(ast, Usub):
            return '-' + wrap_parethesis(ast.a)
        else:
            return '{}({})'.format(ast.__class__.__name__.lower(), compose(ast.a))
    elif isinstance(ast, DoubleToken):
        if isinstance(ast, Add): op = '+' 
        if isinstance(ast, Sub): op = '-' 
        if isinstance(ast, Mul): op = '*' 
        if isinstance(ast, Div): op = '/' 
        if isinstance(ast, Pow): op = '^' 

        return wrap_parethesis(ast.a) + op + wrap_parethesis(ast.b)
    elif isinstance(ast, Variable):
        return ast.name
    elif isinstance(ast, Constant):
        return str(ast.value)
    else:
        raise Exception('Compose error: unknown node type: '+ast.__class__.__name__)