from math_ast import *

def compose(ast: MathAST) -> str:
    if isinstance(ast, Pi):
        return 'pi'
    elif isinstance(ast, Exponenta):
        return 'e'
    elif isinstance(ast, SingleToken):
        return '{}({})'.format(ast.__class__.__name__.lower(), compose(ast.a))
    elif isinstance(ast, DoubleToken):
        if isinstance(ast, Add): op = '+' 
        if isinstance(ast, Sub): op = '-' 
        if isinstance(ast, Mul): op = '*' 
        if isinstance(ast, Div): op = '/' 
        if isinstance(ast, Pow): op = '^' 

        if isinstance(ast.a, LeafToken) or isinstance(ast.a, SingleToken):
            templ = '{1}'
        else:
            templ = '({1})'
        templ += '{0}'
        if isinstance(ast.b, LeafToken) or isinstance(ast.b, SingleToken):
            templ += '{2}'
        else:
            templ += '({2})'

        return templ.format(op, compose(ast.a), compose(ast.b))
    elif isinstance(ast, Variable):
        return ast.name
    elif isinstance(ast, Constant):
        return str(ast.value)
    else:
        raise Exception('Compose error: unknown node type: '+ast.__class__.__name__)