from LoxCallable import LoxCallable
from LoxFunction import LoxFunction

class LoxClass(LoxCallable):
  def __init__(self, name: str, methods: dict[str, LoxFunction]) -> None:
    self.name: str = name
    self.methods: dict[str, LoxFunction] = methods
    
  def __str__(self):
    return self.name
  
  def findMethod(self, name: str) -> LoxFunction:
    if name in self.methods:
      return self.methods.get(name)
    
    return None
  
  def call(self, interpreter, arguments: list[any]) -> any:
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
  