from Expr import Expr, Literal, Grouping, Unary, Binary, Variable, Assign, Logical, Call
from TokenType import TokenType
from Token import Token
from RuntimeError import RuntimeException
from Stmt import Stmt, Expression, Print, Var, Block, If, While, Function, Return
from Environment import Environment
from LoxCallable import LoxCallable
from Return import Return
import time

class Interpreter(Expr.Visitor[object], Stmt.Visitor[None]):
  def __init__(self) -> None:
    self.globals: Environment = Environment()
    self.environment: Environment = self.globals
    self.globals.define("clock", ClockFunction())
  
  def interpret(self, statments: list[Stmt]) -> None:
    from Lox import Lox
    try:
      for statment in statments:
        self.__execute(statment)
    except RuntimeException as error:
      Lox.runtimeError(error)
      
  def visitLiteralExpr(self, expr: Literal) -> any:
    return expr.value
  
  def visitGroupingExpr(self, expr: Grouping) -> any:
    return self.__evaluate(expr.expression)
  
  def visitUnaryExpr(self, expr: Unary) -> any:
    right: any = self.__evaluate(expr.right)
    
    if expr.operator.type == TokenType.MINUS:
      self.__checkNumberOperands(expr.operator, right)
      return -float(right)
    elif expr.operator.type == TokenType.BANG:
      return not self.__isTruthy(right)
    
    return None
  
  def visitBinaryExpr(self, expr: Binary) -> any:
    left: any = self.__evaluate(expr.left)
    right: any = self.__evaluate(expr.right)
    
    if expr.operator.type == TokenType.BANG_EQUAL:
      return not self.__isEqual(left, right)
    elif expr.operator.type == TokenType.EQUAL_EQUAL:
      return self.__isEqual(left, right)
    
    elif expr.operator.type == TokenType.GREATER:
      self.__checkNumberOperands(expr.operator, left, right)
      return float(left) > float(right)
    elif expr.operator.type == TokenType.GREATER_EQUAL:
      self.__checkNumberOperands(expr.operator, left, right)
      return float(left) >= float(right)
    elif expr.operator.type == TokenType.LESS: 
      self.__checkNumberOperands(expr.operator, left, right)
      return float(left) < float(right)
    elif expr.operator.type == TokenType.LESS_EQUAL:
      self.__checkNumberOperands(expr.operator, left, right)
      return float(left) <= float(right)
    
    elif expr.operator.type == TokenType.MINUS:
      self.__checkNumberOperands(expr.operator, left, right)
      return float(left) - float(right)
    
    elif expr.operator.type == TokenType.PLUS:
      if isinstance(left, float) and isinstance(right, float):
        return left + right 
      elif isinstance(left, str) and isinstance(right, str):
        return left + right
      else:
        raise RuntimeException(expr.operator, "Operands must be two numbers or two strings.")
      
    elif expr.operator.type == TokenType.SLASH:
      self.__checkNumberOperands(expr.operator, left, right)
      if float(right) == 0:
        raise RuntimeException(expr.operator, "Division by zero.")
      return float(left) / float(right)
    
    elif expr.operator.type == TokenType.STAR:
      self.__checkNumberOperands(expr.operator, left, right)
      return float(left) * float(right)
    
    return None
  
  def visitExpressionStmt(self, stmt: Expression) -> None:
    self.__evaluate(stmt.expression)
    return None
  
  def visitFunctionStmt(self, stmt:Function) -> None:
    from LoxFunction import LoxFunction
    function: LoxFunction = LoxFunction(stmt, self.environment)
    self.environment.define(stmt.name.lexeme, function)
    return None
  
  def visitPrintStmt(self, stmt: Print) -> None:
    value: any = self.__evaluate(stmt.expression)
    print(self.__stringify(value))
    return None
  
  def visitReturnStmt(self, stmt: Return) -> None:
    value: any = None
    if stmt.value != None:
      value = self.__evaluate(stmt.value)
    
    raise Return(value)
  
  def visitVarStmt(self, stmt: Var) -> None:
    value: any = None
    if stmt.initializer != None:
      value = self.__evaluate(stmt.initializer)
      
    self.environment.define(stmt.name.lexeme, value)
    return None
  
  def visitBlockStmt(self, stmt: Block) -> None:
    self.executeBlock(stmt.statements, Environment(self.environment))
    return None
  
  def visitIfStmt(self, stmt: If) -> None:
    if self.__isTruthy(self.__evaluate(stmt.condition)):
      self.__execute(stmt.thenBranch)
    elif stmt.elseBranch != None:
      self.__execute(stmt.elseBranch)
      
    return None
  
  def visitWhileStmt(self, stmt: While) -> None:
    while self.__isTruthy(self.__evaluate(stmt.condition)):
      self.__execute(stmt.body)
      
    return None
  
  def visitAssignExpr(self, expr: Assign) -> any:
    value: any = self.__evaluate(expr.value)
    self.environment.assign(expr.name, value)
    return value

  def visitCallExpr(self, expr: Call) -> any:
    callee: any = self.__evaluate(expr.callee)
    arguments: list[any] = []
    
    for argument in expr.arguments:
      arguments.append(self.__evaluate(argument))
      
    if not isinstance(callee, LoxCallable):
      raise RuntimeException(expr.paren, "Can only call functions and classes.")
      
    function: LoxCallable = callee
    
    if len(arguments) != function.arity():
      raise RuntimeException(expr.paren, f"Expected {function.arity()} arguments but got {len(arguments)}.")
    
    return function.call(self, arguments)

  def visitGetExpr(self, expr):
    pass  # Implement later

  def visitLogicalExpr(self, expr: Logical) -> any:
    left: any = self.__evaluate(expr.left)
    
    if expr.operator.type == TokenType.OR:
      if self.__isTruthy(left): return left
    else:
      if not self.__isTruthy(left): return left
      
    return self.__evaluate(expr.right)

  def visitSetExpr(self, expr):
    pass  # Implement later

  def visitSuperExpr(self, expr):
    pass  # Implement later

  def visitThisExpr(self, expr):
    pass  # Implement later

  def visitVariableExpr(self, expr: Variable) -> any:
    return self.environment.get(expr.name)
    
  def __evaluate(self, expr: Expr) -> any:
    return expr.accept(self)
  
  def __execute(self, stmt: Stmt) -> None:
    stmt.accept(self)
    
  def executeBlock(self, statments: list[Stmt], environment: Environment) -> None:
    previous: Environment = self.environment
    try:
      self.environment = environment
      
      for statment in statments:
        self.__execute(statment)
        
    finally:
      self.environment = previous
  
  @staticmethod
  def __isTruthy(obj: any) -> bool:
    if obj is None:
        return False
    if isinstance(obj, bool):
        return obj
    return True
  
  @staticmethod
  def __isEqual(a: any, b: any) -> bool:
    if a == None and b == None:
      return True
    
    if a == None:
      return False
    
    return a == b
  
  @staticmethod
  def __checkNumberOperand(operator: Token, operand: any) -> None:
    if isinstance(operand, (int, float)):
      return
    raise RuntimeException(operator, "Operand must be a number.")
  
  @staticmethod
  def __checkNumberOperands(operator: Token, left: any, right: any) -> None:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
      return
    raise RuntimeException(operator, "Operands must be numbers.")
  
  @staticmethod
  def __stringify(obj: any) -> str:
    if obj == None:
      return "nil"
    
    if isinstance(obj, (int, float)):
      text: str = str(obj)
      if text.endswith(".0"):
        text = text[:-2]

      return text
    
    return str(obj)

class ClockFunction(LoxCallable):
  def arity(self) -> int:
    return 0

  def call(self, interpreter: Interpreter, arguments: list[any]) -> float:
      return time.time()
      
  def __str__(self) -> str:
    return "<native fn>"
  