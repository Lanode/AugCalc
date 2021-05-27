from derivative import isDependsOnVar
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

def simplify(n: MathAST) -> MathAST:
    if isinstance(n, LeafToken):
        return n
    
    if not is_var_dependant(n):
    if isinstance(n, SingleToken):
        n.a = simplify(n.a)
        return n
    elif isinstance(n, DoubleToken):
        if isinstance(n, Add):
            if (n.a == 0):
                return n.b
            elif (n.b == 0):
                return n.a
        elif isinstance(n, Mul):
            if (n.a == 0 or n.b == 0):
                return Constant(0)
            elif (n.a == 1):
                return n.b
            elif (n.b == 1):
                return n.a
        elif isinstance(n, Div):
            if (n.a == 0):
                return Constant(0)
            elif (n.b == 1)
