from Expr import Expr, Literal, Grouping, Unary, Binary
from TokenType import TokenType
from Token import Token
from RuntimeError import RuntimeException

class Interpreter(Expr.Visitor[object]):
  def __init__(self):
    pass
  
  def interpret(self, expression: Expr) -> None:
    from Ploxy.Lox import Lox
    try:
      value: object = self.__evaluate(expression)
      print(self.__stringify(value))
    except RuntimeException as error:
      Lox.runtimeError(error)
  def visitLiteralExpr(self, expr: Literal) -> object:
    return expr.value
  
  def visitGroupingExpr(self, expr: Grouping) -> object:
    return self.__evaluate(expr.expression)
  
  def visitUnaryExpr(self, expr: Unary) -> object:
    right: object = self.__evaluate(expr.right)
    
    if expr.operator.type == TokenType.MINUS:
      self.__checkNumberOperands(expr.operator, right)
      return -float(right)
    elif expr.operator.type == TokenType.BANG:
      return not self.__isTruthy(right)
    
    return None
  
  def visitBinaryExpr(self, expr: Binary) -> object:
    left: object = self.__evaluate(expr.left)
    right: object = self.__evaluate(expr.right)
    
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
  
  def __evaluate(self, expr: Expr) -> object:
    return expr.accept(self)
  
  @staticmethod
  def __isTruthy(obj: object) -> bool:
    if obj is None:
        return False
    if isinstance(obj, bool):
        return obj
    return True
  
  @staticmethod
  def __isEqual(a: object, b:object) -> bool:
    if a == None and b == None:
      return True
    
    if a == None:
      return False
    
    return a == b
  
  @staticmethod
  def __checkNumberOperand(operator: Token, operand: object) -> None:
    if isinstance(operand, (int, float)):
      return
    raise RuntimeException(operator, "Operand must be a number.")
  
  @staticmethod
  def __checkNumberOperands(operator: Token, left: object, right: object) -> None:
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
      return
    raise RuntimeException(operator, "Operands must be numbers.")
  
  @staticmethod
  def __stringify(obj: object) -> str:
    if obj == None:
      return "nil"
    
    if isinstance(obj, (int, float)):
      text: str = str(obj)
      if text.endswith(".0"):
        text = text[:-2]

      return text
    
    return str(obj)
  