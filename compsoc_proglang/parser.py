from __future__ import annotations

from lark.lark import Lark
from lark.visitors import Transformer

from . import ast

parser = Lark("""
start: _expr

IDENT: ("-"|"_"|"*"|"+"|LETTER) ("-"|"_"|"*"|"+"|LETTER|DIGIT)*

let: "(" "let" "(" let_binds ")" exprs ")"
let_bind: "(" IDENT _expr ")"
let_binds: let_bind*

lam: "(" "lambda" "(" lam_binds ")" exprs ")"
lam_binds: IDENT*

apply: "(" _expr _expr* ")"

number: NUMBER | SIGNED_NUMBER
ident: IDENT

_expr: let
     | lam
     | apply
     | ident
     | number
     | ESCAPED_STRING

exprs: _expr*

COMMENT: /;.*/

%import common (LETTER, NUMBER, DIGIT, SIGNED_NUMBER, ESCAPED_STRING, WS)
%ignore COMMENT
%ignore WS
""", parser="lalr")


class IntoAST(Transformer):
    def start(self, args):
        return args[0]

    def IDENT(self, args):
        return args

    def number(self, args):
        return ast.Number(float(args[0]))

    def ESCAPED_STRING(self, args):
        return ast.String(args[1:-1])

    def ident(self, args):
        return ast.Ident(args[0])

    def let_bind(self, args):
        return (args[0], args[1])

    def let_binds(self, args):
        return args

    def let(self, args):
        # non terminals passed in as a list
        binds, body = args

        return ast.Let(binds, body)

    def lam(self, args):
        binds, body = args

        return ast.Lambda(binds, body)

    def lam_binds(self, args):
        return args

    def exprs(self, args):
        return args

    def apply(self, args):
        fn, *params = args

        return ast.Apply(fn, params)
