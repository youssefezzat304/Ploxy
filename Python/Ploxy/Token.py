from typing import Any
from .TokenType import TokenType

class Token:
  def __init__(self, type: TokenType, lexeme: str, literal: Any, line: int) -> None:
    self.type = type
    self.lexeme = lexeme
    self.literal = literal
    self.line = line
    
  def __str__(self) -> str:
    return f"{self.type} {self.lexeme} {self.literal}"