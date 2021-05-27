from math_ast import *

def differentiate(f: MathAST, dx: str) -> MathAST:
    if isinstance(f, Differentiate): return differentiate(f.f, f.dx)

    elif isinstance(f, Add): return Add(differentiate(f.a, dx), differentiate(f.b, dx))
    elif isinstance(f, Sub): return Add(differentiate(f.a, dx), differentiate(f.b, dx))
    elif isinstance(f, Div): return Div(Sub(Mul(differentiate(f.a, dx), f.b), Mul(f.a, differentiate(f.b, dx))), Pow(f.b, Constant(2)))

    elif isinstance(f, Pow):
        u = isDependsOnVar(f.a, dx)
        v = isDependsOnVar(f.b, dx)
        if u and not v: 
            return Mul(Mul(Pow(f.a, Sub(f.b, Constant(1))), differentiate(f.a, dx)), f.b) # u(x)^c, c=const
        elif not u and v:   # c^u(x), c=const
            return Mul(Mul(Pow(f.a, f.b), differentiate(f.b, dx)), Ln(f.a))
        elif not u and not v:
            return Constant(0)
        else:
            return Mul(Pow(f.a, Sub(f.b, Constant(1))), Add(Mul(f.b, differentiate(f.a, dx)), Mul(Mul(f.a, Ln(f.a)), differentiate(f.b, dx))))

    elif isinstance(f, Mul):
        u = isDependsOnVar(f.a, dx)
        v = isDependsOnVar(f.b, dx)
        if u and not v:
            return Mul(differentiate(f.a, dx), f.b)
        elif not u and v:  # c^u(x), c=const
            return Mul(f.a, differentiate(f.b, dx))
        elif not u and not v: # c^c, c=const
            return Constant(0)
        else:
            return Add(Mul(differentiate(f.a, dx), f.b), Mul(f.a, differentiate(f.b, dx)))

    elif isinstance(f, SingleToken):
        
        if isinstance(f, Sin): d = Cos(f.a)
        if isinstance(f, Cos): d = Usub(Sin(f.a))
        if isinstance(f, Tg): d = Div(Constant(1), Pow(Cos(f.a), Constant(2)))
        if isinstance(f, Ctg): d = Usub(Div(Constant(1), Pow(Sin(f.a), Constant(2))))
        if isinstance(f, Abs): d = Div(f.a, Abs(f.a))
        if isinstance(f, Ln): d = Div(Constant(1), f.a)
        if isinstance(f, Sqrt): d = Div(Constant(1), Mul(Constant(2), Sqrt(f.a)))
        if isinstance(f, Usub): d = Usub(differentiate(f.a, dx))
        if isinstance(f, Arcsin): d = Div(Constant(1), Sqrt(Sub(Constant(1), Pow(f.a, Constant(2)))))
        if isinstance(f, Arccos): d = Usub(Div(Constant(1), Sqrt(Sub(Constant(1), Pow(f.a, Constant(2))))))
        if isinstance(f, Arctg): d = Div(Constant(1), Sub(Constant(1), Pow(f.a, Constant(2))))
        if isinstance(f, Arcctg): d = Usub(Div(Constant(1), Sub(Constant(1), Pow(f.a, Constant(2)))))

        if (isLeaf(f.a)): 
            return d 
        else: 
            return Mul(d, differentiate(f.a, dx))

    elif isinstance(f, Variable): 
        if (f.name == dx):
            return Constant(1) 
        else:
            return Constant(0)
    elif isinstance(f, Constant): 
        return Constant(0)
    elif isinstance(f, Pi) or isinstance(f, Exponenta): 
        return Constant(0)
    else:
        print("ERROR")

def isLeaf(e: MathAST) -> bool:
    if isinstance(e, Variable) or isinstance(e, Constant): 
        return True
    elif isinstance(e, Pi) or isinstance(e, Exponenta):
        return True
    else:
        return False

def isDependsOnVar(tree: MathAST, dx: str) -> bool:
    if isinstance(tree, DoubleToken):
        if isinstance(tree.a, Variable):
            if tree.a.name == dx: 
                a = True 
            else: 
                a = False
        else:
            a = isDependsOnVar(tree.a, dx)
        if isinstance(tree.b, Variable):
            if tree.b.name == dx: 
                b = True 
            else: 
                b = False 
        else:
            b = isDependsOnVar(tree.b, dx)

        return a or b
        # (e.a match {
        #     case Variable(name) => if(name == dx) true else false
        #     case _ => isDependsOnVar(e.a)
        # })||(e.b match {
        #     case Variable(name) => if(name == dx) true else false
        #     case _ => isDependsOnVar(e.b)
        # })
    elif isinstance(tree, SingleToken): return isDependsOnVar(tree.a, dx)
    elif isinstance(tree, Variable): 
        if tree.name == dx: 
            return True
        else:
            return False
    else: 
        return False