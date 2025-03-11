from typing import Optional
from Token import Token
from TokenType import TokenType

class Scanner:
  def __init__(self, source: str) -> None:
    
    self.keywords: dict[str, TokenType] = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }
    
    self.source: str = source
    self.tokens: list[Token] = []
    self.start: int = 0
    self.current: int = 0
    self.line: int = 1
    
  def scanTokens(self) -> list[Token]:
    while not self.__isAtEnd():
      self.start = self.current
      self.__scanToken()
      
    self.tokens.append(Token(TokenType.EOF, "", None, self.line))
    return self.tokens
  
## /> scan-token  ###
  def __scanToken(self) -> None:
    c = self.__advance()
    if   c == '(': self.__addToken(TokenType.LEFT_PAREN)
    elif c == ')': self.__addToken(TokenType.RIGHT_PAREN)
    elif c == '{': self.__addToken(TokenType.LEFT_BRACE)
    elif c == '}': self.__addToken(TokenType.RIGHT_BRACE)
    elif c == ',': self.__addToken(TokenType.COMMA)
    elif c == '.': self.__addToken(TokenType.DOT)
    elif c == '-': self.__addToken(TokenType.MINUS)
    elif c == '+': self.__addToken(TokenType.PLUS)
    elif c == ';': self.__addToken(TokenType.SEMICOLON)
    elif c == '*': self.__addToken(TokenType.STAR)

    elif c == '!':
        self.__addToken(
            TokenType.BANG_EQUAL if self.__match('=') else TokenType.BANG
        )
    elif c == '=':
        self.__addToken(
            TokenType.EQUAL_EQUAL if self.__match('=') else TokenType.EQUAL
        )
    elif c == '<':
        self.__addToken(
            TokenType.LESS_EQUAL if self.__match('=') else TokenType.LESS
        )
    elif c == '>':
        self.__addToken(
            TokenType.GREATER_EQUAL if self.__match('=') else TokenType.GREATER
        )
      
      
    elif c == "/":
      if self.__match("/"):
        while self.__peek() != "\n" and not self.__isAtEnd():
          self.__advance()
        else:
          self.__addToken(TokenType.SLASH)
          
    elif c in {" ", "\r", "\t"}:
      return
    elif c == "\n":
      self.line += 1
      
    elif c == '"':
      self.__string()
    else:
      if self.__isDigit(c):
        self.__number()
      elif self.__isAlpha(c):
        self.__identifier()
      else:
        from Lox import Lox
        Lox.errorl(self.line, "Unexpected character")
## /< scan-token ###

  def __identifier(self) -> None:
    while self.__isAlphaNumeric(self.__peek()): self.__advance()
    
    text: str = self.source[self.start:self.current]
    type: TokenType = self.keywords.get(text)
    if type is None: 
      type = TokenType.IDENTIFIER
    self.__addToken(type)
    
  def __number(self) -> None:
    while self.__isDigit(self.__peek()):
      self.__advance()
    
    if self.__peek() == "." and self.__isDigit(self.__peekNext()):
      self.__advance()
      
      while self.__isDigit(self.__peek()):
        self.__advance()
        
    self.__addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))
    
  def __string(self) -> None:
    from Lox import Lox
    while self.__peek() != '"' and not self.__isAtEnd():
      if self.__peek() == "\n": self.line += 1    
      self.__advance()
    
    if self.__isAtEnd():
      Lox.errorl(self.line, "Unterminated string.")
      return
    
    self.__advance()
    
    value = self.source[self.start + 1:self.current - 1]
    self.__addToken(TokenType.STRING, value)
     
  def __match(self, expected) -> bool:
    if(self.__isAtEnd()): return False
    if(self.source[self.current] != expected): return False
    
    self.current += 1
    return True
  
  def __peek(self) -> str:
    if self.__isAtEnd(): return "\0"
    return self.source[self.current]
  
  def __peekNext(self) -> str:
    if self.current + 1 >= len(self.source): return '\0'

    return self.source[self.current + 1]
  
  def __isAlpha(self, c) -> bool:
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z') or c == '_'
  
  def __isAlphaNumeric(self, c) -> bool:
    return self.__isAlpha(c) or self.__isDigit(c)
    
  def __isDigit(self, c):
    return c >= "0" and c <= "9"
  
  def __isAtEnd(self) -> bool:
    return self.current >= len(self.source)
  
  def __advance(self) -> str:
    self.current += 1
    return self.source[self.current - 1]
  
  def __addToken(self, type: TokenType, literal: Optional[any] = None) -> None:
    text = self.source[self.start:self.current]
    self.tokens.append(Token(type, text, literal, self.line))      
