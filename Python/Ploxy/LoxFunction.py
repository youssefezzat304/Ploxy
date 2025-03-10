from LoxCallable import LoxCallable
from Stmt import Function
from Interpreter import Interpreter
from Environment import Environment
from Return import Return

class LoxFunction(LoxCallable):
  def __init__(self, declaration: Function, closure: Environment) -> None:
    self.closure: Environment = closure
    self.declaration: Function = declaration
    
  def arity(self) -> int:
    return len(self.declaration.params)
  
  def call(self, interpreter: Interpreter, arguments: list[any]) -> any:
    environment: Environment = Environment(self.closure)
    for i, param in enumerate(self.declaration.params):
      environment.define(param.lexeme, arguments[i])
      
    try:
      interpreter.executeBlock(self.declaration.body, environment)
    except Return as returnValue:
      return returnValue.value
      
    return None
  
  def __str__(self) -> str:
    return f"<fn {self.declaration.name.lexeme}>"