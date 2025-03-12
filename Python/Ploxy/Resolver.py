from Expr import Expr, Variable, Assign, Binary, Grouping, Call, Literal, Logical, Unary, Get, Set, Super, This
from Stmt import Stmt, Block, Var, Function, Expression, If, Print, While, Return, Class
from Interpreter import Interpreter
from collections import deque
from Token import Token
from enum import Enum

class FunctionType(Enum):
  NONE = "NONE"
  FUNCTION = "FUNCTION"
  INITIALIZER = "INITIALIZER"
  METHOD = "METHOD"
  
class ClassType(Enum):
  NONE = "NONE"
  CLASS = "CLASS"
  SUBCLASS = "SUBCLASS"

class Resolver(Expr.Visitor[None], Stmt.Visitor[None]):
  def __init__(self, interpreter: Interpreter):
    self.interpreter: Interpreter = interpreter
    self.scopes: deque = deque()
    self.currentFunction: FunctionType = FunctionType.NONE
    self.currentClass: ClassType = ClassType.NONE
    
  def resolve(self, statments: list[Stmt]) -> None:
    for statment in statments:
      self.__resolveStmt(statment)
      
  def visitBlockStmt(self, stmt: Block) -> None:
    self.beginScope()
    self.resolve(stmt.statements)
    self.endScope()
    return None
  
  def visitClassStmt(self, stmt: Class) -> None:
    from Lox import Lox
    enclosingClass: ClassType = self.currentClass
    self.currentClass = ClassType.CLASS
    
    self.__declare(stmt.name)
    self.__define(stmt.name)
    
    if stmt.superclass != None and stmt.name.lexeme == stmt.superclass.name.lexeme:
      Lox.errort(stmt.superclass.name, "A class can't inherit from itself.")
      
    if stmt.superclass != None:
      self.currentClass = ClassType.SUBCLASS
      self.__resolveExpr(stmt.superclass)
      
    if stmt.superclass != None:
      self.beginScope()
      self.scopes[-1]["super"] = True
      
    self.beginScope()
    self.scopes[-1]["this"] = True
    
    for method in stmt.methods:
      declaration: FunctionType = FunctionType.METHOD
      if method.name.lexeme == "init":
        declaration = FunctionType.INITIALIZER
        
      self.__resolveFunction(method, declaration)
      
    self.endScope()
    self.currentClass = enclosingClass
    return None
  
  def visitExpressionStmt(self, stmt: Expression) -> None:
    self.__resolveExpr(stmt.expression)
    return None
  
  def visitFunctionStmt(self, stmt: Function) -> None:
    self.__declare(stmt.name)
    self.__define(stmt.name)
    self.__resolveFunction(stmt, FunctionType.FUNCTION)
    return None
  
  def visitIfStmt(self, stmt: If) -> None:
    self.__resolveExpr(stmt.condition)
    self.__resolveStmt(stmt.thenBranch)
    if stmt.elseBranch != None:
      self.__resolveStmt(stmt.elseBranch)
    return None
  
  def visitPrintStmt(self, stmt: Print) -> None:
    self.__resolveExpr(stmt.expression)
    return None
  
  def visitReturnStmt(self, stmt: Return) -> None:
    from Lox import Lox
    if self.currentFunction == FunctionType.NONE:
      Lox.errort(stmt.keyword, "Can't return from top-level code.")
      
    if stmt.value != None:
      if self.currentFunction == FunctionType.INITIALIZER:
        Lox.errort(stmt.keyword, "Can't return a value from an initializer.")
        
      self.__resolveExpr(stmt.value)
      
    return None
  
  def visitVarStmt(self, stmt: Var) -> None:
    self.__declare(stmt.name)
    if stmt.initializer != None:
      self.__resolveExpr(stmt.initializer)
      
    self.__define(stmt.name)
    return None
  
  def visitWhileStmt(self, stmt: While) -> None:
    self.__resolveExpr(stmt.condition)
    self.__resolveStmt(stmt.body)
    return None
  
  def visitAssignExpr(self, expr: Assign) -> None:
    self.__resolveExpr(expr.value)
    self.__resolveLocal(expr, expr.name)
    return None
  
  def visitUnaryExpr(self, expr: Unary) -> None:
    self.__resolveExpr(expr.right)
    return None
  
  def visitBinaryExpr(self, expr: Binary) -> None:
    self.__resolveExpr(expr.left)
    self.__resolveExpr(expr.right)
    return None
  
  def visitCallExpr(self, expr: Call) -> None:
    self.__resolveExpr(expr.callee)
    
    for argument in expr.arguments:
      self.__resolveExpr(argument)
    
    return None
  
  def visitGetExpr(self, expr: Get) -> None:
    self.__resolveExpr(expr.object)
    return None
  
  def visitGroupingExpr(self, expr: Grouping) -> None:
    self.__resolveExpr(expr.expression)
    return None
  
  def visitLiteralExpr(self, expr: Literal) -> None:
    return None
  
  def visitLogicalExpr(self, expr: Logical) -> None:
    self.__resolveExpr(expr.left)
    self.__resolveExpr(expr.right)
    return None
  
  def visitSetExpr(self, expr: Set) -> None:
    self.__resolveExpr(expr.value)
    self.__resolveExpr(expr.object)
    return None
  
  def visitSuperExpr(self, expr: Super) -> None:
    from Lox import Lox
    if self.currentClass == ClassType.NONE:
      Lox.errort(expr.keyword, "Can't use 'super' outside of a class.")
    elif self.currentClass != ClassType.SUBCLASS:
      Lox.errort(expr.keyword, "Can't use 'super' in a class with no superclass.")
      
    self.__resolveLocal(expr, expr.keyword)
    return None
  
  def visitVariableExpr(self, expr: Variable) -> None:
    from Lox import Lox
    if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
      isDeclared, _ = self.scopes[-1][expr.name.lexeme]
      if not isDeclared:
        Lox.errort(expr.name, "Can't read local variable in its own initializer.")
        
      self.scopes[-1][expr.name.lexeme] = (isDeclared, True)
      
    self.__resolveLocal(expr, expr.name)
    return None
  
  def visitThisExpr(self, expr: This) -> None:
    from Lox import Lox
    if self.currentClass == ClassType.NONE:
      Lox.errort(expr.keyword, "Can't use 'this' outside of a class.")
      return None
    
    self.__resolveLocal(expr, expr.keyword)
    return None
  
  def __resolveStmt(self, stmt: Stmt) -> None:
    stmt.accept(self)
    
  def __resolveExpr(self, expr: Expr) -> None:
    expr.accept(self)
    
  def __declare(self, name: Token) -> None:
    from Lox import Lox
    if not self.scopes:
      return
    scope: dict[str, bool] = self.scopes[-1]
    if name.lexeme in scope:
      Lox.errort(name, "Already variable with this name in this scope.")
      
    scope[name.lexeme] = (False, False)
    
  def __define(self, name: Token) -> None:
    if not self.scopes:
      return
    self.scopes[-1][name.lexeme] = (True, False)
    
  def __resolveLocal(self, expr: Expr, name: Token) -> None:
    for i in range(len(self.scopes) - 1, -1, -1):
      if name.lexeme in self.scopes[i]:
        self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
        return
      
  def __resolveFunction(self, function: Function, type: FunctionType) -> None:
    enclosingFunction: FunctionType = self.currentFunction
    self.currentFunction = type
    self.beginScope()
    for param in function.params:
      self.__declare(param)
      self.__define(param)
      
    self.resolve(function.body)
    self.endScope()
    self.currentFunction = enclosingFunction
    
  def beginScope(self) -> None:
    self.scopes.append({})
    
  def endScope(self) -> None:
    self.scopes.pop()
    