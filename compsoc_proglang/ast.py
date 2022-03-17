from __future__ import annotations

from typing import Any, Protocol

from dataclasses import dataclass


class ASTNode(Protocol):
    def eval(self, env: dict[str, Any]) -> Any:
        ...

@dataclass
class Ident(ASTNode):
    name: str

    def eval(self, env: dict[str, Any]) -> Any:
        return env[self.name]

@dataclass
class Number(ASTNode):
    value: float

    def eval(self, env: dict[str, Any]) -> Any:
        return self.value

@dataclass
class String(ASTNode):
    value: str

    def eval(self, env: dict[str, Any]) -> Any:
        return self.value

@dataclass
class Let(ASTNode):
    binds: list[tuple[str, ASTNode]]
    exprs: list[ASTNode]

    def eval(self, env: dict[str, Any]) -> Any:
        new_env = env.copy()

        for name, node in self.binds:
            new_env[name] = node.eval(env)

        last_expr = None
        for expr in self.exprs:
            last_expr = expr.eval(new_env)

        return last_expr


@dataclass
class Lambda(ASTNode):
    names: list[str]
    exprs: list[ASTNode]

    def eval(self, env: dict[str, Any]) -> Any:
        def inner(params):
            new_env = env.copy()

            assert len(params) == len(self.names)

            for name, value in zip(self.names, params):
                # don't eval parameters, they're evalled at the call site
                new_env[name] = value

            last_expr = None
            for expr in self.exprs:
                last_expr = expr.eval(new_env)

            return last_expr
        return inner


@dataclass
class Apply(ASTNode):
    fn: ASTNode
    params: list[ASTNode]

    def eval(self, env: dict[str, Any]) -> Any:
        fn = self.fn.eval(env)

        params = []
        for node in self.params:
            params.append(node.eval(env))

        return fn(params)
