from LoxClass import LoxClass
from Token import Token
from RuntimeError import RuntimeException

class LoxInstance:
  def __init__(self, Klass: LoxClass) -> None:
    self.Klass: LoxClass = Klass
    self.fields: dict[str, any] = {}
    
  def get(self, name: Token) -> any:
    from LoxFunction import LoxFunction
    if name.lexeme in self.fields:
      return self.fields.get(name.lexeme)
    
    method: LoxFunction = self.Klass.findMethod(name.lexeme)
    if method != None: return method.bind(self)
    
    raise RuntimeException(name, f"Undefined property '{name.lexeme}'.")
  
  def set(self, name: Token, value: any) -> None:
    self.fields[name.lexeme] = value
    
  def __str__(self):
    return self.Klass.name + " instance"
  