from typing import TYPE_CHECKING
from .LoxCallable import LoxCallable
from .Stmt import Function
from .Environment import Environment
from .Return import Return

if TYPE_CHECKING:
  from .LoxInstance import LoxInstance
  from .Interpreter import Interpreter

class LoxFunction(LoxCallable):
  def __init__(self, declaration: Function, closure: Environment, isInitializer: bool) -> None:
    self.isInitializer = isInitializer
    self.closure: Environment = closure
    self.declaration: Function = declaration
    
  def bind(self, instance: 'LoxInstance') -> 'LoxFunction':
    environment: Environment = Environment(self.closure)
    environment.define("this", instance)
    return LoxFunction(self.declaration, environment, self.isInitializer)
    
  def arity(self) -> int:
    return len(self.declaration.params)
  
  def call(self, interpreter: 'Interpreter', arguments: list[any]) -> any:
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
  