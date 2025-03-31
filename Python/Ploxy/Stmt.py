# This file is auto-generated by __defineAst.

from typing import Protocol, TypeVar
from abc import ABC, abstractmethod
from .Token import Token
from .Expr import Expr, Variable

R = TypeVar('R')

class Stmt(ABC):
    class Visitor(Protocol[R]):
       @abstractmethod
       def visitBlockStmt(self, stmt: 'Block'):
          pass
       @abstractmethod
       def visitClassStmt(self, stmt: 'Class'):
          pass
       @abstractmethod
       def visitExpressionStmt(self, stmt: 'Expression'):
          pass
       @abstractmethod
       def visitFunctionStmt(self, stmt: 'Function'):
          pass
       @abstractmethod
       def visitIfStmt(self, stmt: 'If'):
          pass
       @abstractmethod
       def visitPrintStmt(self, stmt: 'Print'):
          pass
       @abstractmethod
       def visitReturnStmt(self, stmt: 'Return'):
          pass
       @abstractmethod
       def visitVarStmt(self, stmt: 'Var'):
          pass
       @abstractmethod
       def visitWhileStmt(self, stmt: 'While'):
          pass

    @abstractmethod
    def accept(self, visitor: 'Expr.Visitor[R]') -> R:
        raise NotImplementedError()

class Block(Stmt):
    def __init__(self, statements: list[Stmt]) -> None:
        self.statements = statements

    def accept(self, visitor) -> R:
        return visitor.visitBlockStmt(self)

class Class(Stmt):
    def __init__(self, name: Token, superclass: Variable, methods: list['Function']) -> None:
        self.name = name
        self.superclass = superclass
        self.methods = methods

    def accept(self, visitor) -> R:
        return visitor.visitClassStmt(self)

class Expression(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor) -> R:
        return visitor.visitExpressionStmt(self)

class Function(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]) -> None:
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor) -> R:
        return visitor.visitFunctionStmt(self)

class If(Stmt):
    def __init__(self, condition: Expr, thenBranch: Stmt, elseBranch: Stmt) -> None:
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor) -> R:
        return visitor.visitIfStmt(self)

class Print(Stmt):
    def __init__(self, expression: Expr) -> None:
        self.expression = expression

    def accept(self, visitor) -> R:
        return visitor.visitPrintStmt(self)

class Return(Stmt):
    def __init__(self, keyword: Token, value: Expr) -> None:
        self.keyword = keyword
        self.value = value

    def accept(self, visitor) -> R:
        return visitor.visitReturnStmt(self)

class Var(Stmt):
    def __init__(self, name: Token, initializer: Expr) -> None:
        self.name = name
        self.initializer = initializer

    def accept(self, visitor) -> R:
        return visitor.visitVarStmt(self)

class While(Stmt):
    def __init__(self, condition: Expr, body: Stmt) -> None:
        self.condition = condition
        self.body = body

    def accept(self, visitor) -> R:
        return visitor.visitWhileStmt(self)

