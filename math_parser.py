from math_ast import *
from typing import *
from enum import IntEnum, auto
import re

class TokenTypes(IntEnum):
    NAMED_FUNCTION = auto()
    CONSTANT = auto()
    OPERATOR = auto()
    LEFT_PARENTHESIS = auto()
    RIGHT_PARENTHESIS = auto()
    NUMBER = auto()
    VARIABLE = auto()

# class stack(list):
#     # def 
#     pass

rules = [
    {
        'key': r"sin|cos|tg|ctg|log|sqrt",
        'type': TokenTypes.NAMED_FUNCTION,
        'data': {
            'args': 1,
            'precedence': 4,
            'isLeftAssociative': True
        }
    },
    {
        'key': r"pi|e",
        'type': TokenTypes.CONSTANT
    },
    {
        'key': r"[\^]",
        'type': TokenTypes.OPERATOR,
        'data': {
            'args': 2,
            'precedence': 3,
            'isLeftAssociative': True
        }
    },
    {
        'key': r"[*\/]",
        'type': TokenTypes.OPERATOR,
        'data': {
            'args': 2,
            'precedence': 2,
            'isLeftAssociative': True
        }
    },
    {
        'key': r"[+-]",
        'type': TokenTypes.OPERATOR,
        'data': {
            'args': 2,
            'precedence': 1,
            'isLeftAssociative': True
        }
    },
    { 'key': r"[([]", 'type': TokenTypes.LEFT_PARENTHESIS },
    { 'key': r"[)\]]", 'type': TokenTypes.RIGHT_PARENTHESIS },
    { 'key': r"[0-9.,]+", 'type': TokenTypes.NUMBER },
    { 'key': r"[a-zA-Z]", 'type': TokenTypes.VARIABLE }
]

def print_tokens(t):
    for x in t:
        print(x[0], end=' ')
    print()

def tokenize(s: str) -> List[Tuple[str, Dict]]:
    output:  List[Tuple[str, Dict]] = list()
    start = 0
    while start < len(s):
        for rule in rules:
            m = re.match(rule['key'], s[start:])
            if m is not None:
                output.append((m.group(0), rule))
                start = start+m.end()
                break
        else:
            raise Exception("Tokenization error near {}: {}".format(start, s[start:]))
    #print_tokens(output)
    return output

def shunting_yard(tokens: List[Tuple[str, Dict]]) -> List[Tuple[str, Dict]]:
    stack = list()
    out = list()

    for token in tokens:
        if token[1]['type'] in (TokenTypes.CONSTANT, TokenTypes.NUMBER, TokenTypes.VARIABLE):
            out.append(token)
        elif token[1]['type'] == TokenTypes.NAMED_FUNCTION:
            stack.append(token)
        elif token[1]['type'] == TokenTypes.OPERATOR:
            while ((len(stack) > 0) #(stack[len(stack)][1]['type'] == TokenTypes.OPERATOR) # ?????
                  and (stack[len(stack)-1][1]['type'] != TokenTypes.LEFT_PARENTHESIS)
                  and ((stack[len(stack)-1][1]['data']['precedence'] > token[1]['data']['precedence']) 
                      or (stack[len(stack)-1][1]['data']['precedence'] == token[1]['data']['precedence'] and token[1]['data']['isLeftAssociative']))):
                out.append(stack.pop())
            stack.append(token)
        elif token[1]['type'] == TokenTypes.LEFT_PARENTHESIS:
            stack.append(token)
        elif token[1]['type'] == TokenTypes.RIGHT_PARENTHESIS:
            while (stack[len(stack)-1][1]['type'] != TokenTypes.LEFT_PARENTHESIS) or (len(stack) == 0):
                out.append(stack.pop())
            # If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
            if len(stack) == 0:
                raise Exception('ShunYard error: no right parenthesis')
            if stack[len(stack)-1][1]['type'] == TokenTypes.LEFT_PARENTHESIS: # нужно ли?
                stack.pop()
            if stack[len(stack)-1][1]['type'] == TokenTypes.NAMED_FUNCTION:
                out.append(stack.pop())
    while len(stack) > 0:
        out.append(stack.pop())

    #print_tokens(out)

def shunting_yard_ast(tokens: List[Tuple[str, Dict]]) -> MathAST:
    stack = list()
    out = list()

    def op_add(op: str):
        b = out.pop()
        a = out.pop()
        if op[0] == '+':
            out.append(Add(a, b))
        elif op[0] == '-':
            out.append(Sub(a, b))
        elif op[0] == '*':
            out.append(Mul(a, b))
        elif op[0] == '/':
            out.append(Div(a, b))
        elif op[0] == '^':
            out.append(Pow(a, b))

    for token in tokens:
        if token[1]['type'] in (TokenTypes.CONSTANT, TokenTypes.NUMBER, TokenTypes.VARIABLE):
            if token[1]['type'] == TokenTypes.CONSTANT:
                for x in constants:
                    if token[0] == x.__name__.lower():
                        out.append(x())
                        break
            elif token[1]['type'] == TokenTypes.NUMBER:
                out.append(Constant(int(token[0])))
            elif token[1]['type'] == TokenTypes.VARIABLE:
                out.append(Variable(token[0]))
            #out.append(token)
        elif token[1]['type'] == TokenTypes.NAMED_FUNCTION:
            stack.append(token)
        elif token[1]['type'] == TokenTypes.OPERATOR:
            while ((len(stack) > 0) #(stack[len(stack)][1]['type'] == TokenTypes.OPERATOR) # ?????
                  and (stack[len(stack)-1][1]['type'] != TokenTypes.LEFT_PARENTHESIS)
                  and ((stack[len(stack)-1][1]['data']['precedence'] > token[1]['data']['precedence']) 
                      or (stack[len(stack)-1][1]['data']['precedence'] == token[1]['data']['precedence'] and token[1]['data']['isLeftAssociative']))):
                op_add(stack.pop()[0])
            stack.append(token)
        elif token[1]['type'] == TokenTypes.LEFT_PARENTHESIS:
            stack.append(token)
        elif token[1]['type'] == TokenTypes.RIGHT_PARENTHESIS:
            while (stack[len(stack)-1][1]['type'] != TokenTypes.LEFT_PARENTHESIS) or (len(stack) == 0):
                op_add(stack.pop()[0])
            # If the stack runs out without finding a left parenthesis, then there are mismatched parentheses.
            if len(stack) == 0:
                raise Exception('ShunYard error: no right parenthesis')
            if stack[len(stack)-1][1]['type'] == TokenTypes.LEFT_PARENTHESIS: # нужно ли?
                stack.pop()
            if stack[len(stack)-1][1]['type'] == TokenTypes.NAMED_FUNCTION:
                fun = stack.pop()
                a = out.pop()
                for x in functions:
                    if fun[0] == x.__name__.lower():
                        out.append(x(a))
                        break
    while len(stack) > 0:
        op_add(stack.pop()[0])

    #print(out[0])

    return out[0]

# def rpn_to_ast(tokens):
#     stack = list()
#     for token in tokens:
#         if token[1]['type'] in (TokenTypes.CONSTANT, TokenTypes.NUMBER, TokenTypes.VARIABLE):
#             stack.append(token)
#         if token[1]['type'] in (TokenTypes.OPERATOR, TokenTypes.NAMED_FUNCTION):
            

def parse(s: str) -> MathAST:
    prepare = ("".join(s.split())).lower()
    tokens = tokenize(prepare)
    return shunting_yard_ast(tokens) 

#shunting_yard_ast(tokenize('1+5-4*a*(3/x)^sin(3)'))