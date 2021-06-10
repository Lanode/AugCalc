from dataclasses import dataclass
import typing

class MathAST: pass

class LeafToken (MathAST): pass

@dataclass
class SingleToken (MathAST):
    a: MathAST

@dataclass
class DoubleToken (MathAST):
    a: MathAST
    b: MathAST

class Pi (LeafToken): pass
class Exponenta (LeafToken): pass

class Sin (SingleToken): pass
class Cos (SingleToken): pass
class Tg (SingleToken): pass
class Ctg (SingleToken): pass
class Ln (SingleToken): pass
class Abs (SingleToken): pass
class Usub (SingleToken): pass
class Arcsin (SingleToken): pass
class Arccos (SingleToken): pass
class Arctg (SingleToken): pass
class Arcctg (SingleToken): pass
class Sqrt (SingleToken): pass

class Mul (DoubleToken): pass
class Add (DoubleToken): pass
class Sub (DoubleToken): pass
class Div (DoubleToken): pass
class Pow (DoubleToken): pass

@dataclass
class Variable (LeafToken):
    name: str
@dataclass
class Constant (LeafToken):
    value: float

@dataclass
class Differentiate (MathAST): 
    f: MathAST
    dx: Variable

constants: typing.List[typing.Type[LeafToken]] = [Pi, Exponenta]
functions: typing.List[typing.Type[SingleToken]] = [Sin, Cos, Tg, Ln, Abs, Usub, Arcsin, Arccos, Arctg, Arcctg]