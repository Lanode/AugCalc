from math_ast import *
import typing as t

def detect_vars(f: MathAST) -> t.List[Variable]:
    vars: t.List[Variable] = list()
    def walk(f):
        if isinstance(f, Variable): 
            for v in vars:
                if v.name == f.name:
                    break
            else:
                vars.append(f)
        elif isinstance(f, SingleToken): 
            walk(f.a)
        elif isinstance(f, DoubleToken): 
            walk(f.a)
            walk(f.b)
    walk(f)
    return vars

def is_depends_on_dx(tree: MathAST, dx: str) -> bool:
    if isinstance(tree, DoubleToken):
        if isinstance(tree.a, Variable):
            if tree.a.name == dx: 
                a = True 
            else: 
                a = False
        else:
            a = is_depends_on_dx(tree.a, dx)
        if isinstance(tree.b, Variable):
            if tree.b.name == dx: 
                b = True 
            else: 
                b = False 
        else:
            b = is_depends_on_dx(tree.b, dx)

        return a or b
        # (e.a match {
        #     case Variable(name) => if(name == dx) true else false
        #     case _ => isDependsOnVar(e.a)
        # })||(e.b match {
        #     case Variable(name) => if(name == dx) true else false
        #     case _ => isDependsOnVar(e.b)
        # })
    elif isinstance(tree, SingleToken): return is_depends_on_dx(tree.a, dx)
    elif isinstance(tree, Variable): 
        if tree.name == dx: 
            return True
        else:
            return False
    else: 
        return False

def is_var_dependant(tree: MathAST) -> bool:
    if isinstance(tree, DoubleToken):
        a = is_var_dependant(tree.a)
        b = is_var_dependant(tree.b)
        return a or b
    elif isinstance(tree, SingleToken): 
        return is_var_dependant(tree.a)
    elif isinstance(tree, Variable) or isinstance(tree, (Pi, Exponenta)): 
        return True
    else: 
        return False

def is_leaf(e: MathAST) -> bool:
    if isinstance(e, Variable) or isinstance(e, Constant): 
        return True
    elif isinstance(e, Pi) or isinstance(e, Exponenta):
        return True
    else:
        return False