from LoxCallable import LoxCallable
from Stmt import Function
from Environment import Environment
from LoxInstance import LoxInstance
from Return import Return

class LoxFunction(LoxCallable):
  def __init__(self, declaration: Function, closure: Environment, isInitializer: bool) -> None:
    self.isInitializer = isInitializer
    self.closure: Environment = closure
    self.declaration: Function = declaration
    
  def bind(self, instance: LoxInstance):
    environment: Environment = Environment(self.closure)
    environment.define("this", instance)
    return LoxFunction(self.declaration, environment, self.isInitializer)
    
  def arity(self) -> int:
    return len(self.declaration.params)
  
  def call(self, interpreter, arguments: list[any]) -> any:
    environment: Environment = Environment(self.closure)
    for i, param in enumerate(self.declaration.params):
      environment.define(param.lexeme, arguments[i])
      
    try:
      interpreter.executeBlock(self.declaration.body, environment)
    except Return as returnValue:
      if self.isInitializer: return self.closure.getAt(0, "this")
      
      return returnValue.value
    
    if self.isInitializer:
      return self.closure.getAt(0, "this")
      
    return None
  
  def __str__(self) -> str:
    return f"<fn {self.declaration.name.lexeme}>"
  