from .ast import *
from .parser import *
from .builtins import *

def my_eval(program: str) -> Any:
    parse_tree = parser.parse(program)
    ast: ASTNode = IntoAST(visit_tokens=True).transform(parse_tree)
    return ast.eval(mylang_builtins)

def repl():
    from prompt_toolkit import prompt
    while True:
        inp = prompt("> ")
        out = my_eval(inp)
        print(out)
