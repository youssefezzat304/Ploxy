from Token import Token
from RuntimeError import RuntimeException

class Environment:
  def __init__(self, enclosing = None) -> None:
    self.enclosing: Environment = enclosing
    self.values: dict[str, any] = {}
    
    
  def get(self, name: Token) -> any:
    if name.lexeme in self.values:
      return self.values.get(name.lexeme)
    
    if self.enclosing != None:
      return self.enclosing.get(name)
    
    raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")
    
  def define(self, name:str, value: any) -> None:
    self.values[name] = value
    
  def assign(self, name: Token, value: any) -> None:
    if name.lexeme in self.values:
      self.values[name.lexeme] = value
      return
    
    if self.enclosing != None:
      self.enclosing.assign(name, value)
      
    raise RuntimeException(name, f"Undefined variable '{name.lexeme}'.")
    