from typing import TYPE_CHECKING
from .LoxCallable import LoxCallable
from .LoxFunction import LoxFunction

if TYPE_CHECKING:
  from Interpreter import Interpreter

class LoxClass(LoxCallable):
  def __init__(self, name: str, superclass: 'LoxClass', methods: dict[str, LoxFunction]) -> None:
    self.superclass: 'LoxClass' = superclass
    self.name: str = name
    self.methods: dict[str, LoxFunction] = methods
    
  def __str__(self):
    return self.name
  
  def findMethod(self, name: str) -> LoxFunction:
    if name in self.methods:
      return self.methods.get(name)
    
    if self.superclass != None:
      return self.superclass.findMethod(name)
    
    return None
  
  def call(self, interpreter: 'Interpreter', arguments: list[any]) -> any:
    from LoxInstance import LoxInstance
    instance: LoxInstance = LoxInstance(self)
    initializer: LoxFunction = self.findMethod("init")
    if initializer != None:
      initializer.bind(instance).call(interpreter, arguments)
    
    return instance
    
  def arity(self) -> int:
    initializer: LoxFunction = self.findMethod("init")
    if initializer == None:
      return 0
    
    return initializer.arity()
  