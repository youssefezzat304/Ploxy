from Token import Token
from Expr import Expr, Binary, Unary, Literal, Grouping
from TokenType import TokenType


class Parser:
  class ParseError(Exception):
    pass
  
  def __init__(self, tokens: list[Token]):
    self.tokens: list[Token] = tokens
    self.current: int = 0
        
  def __expression(self) -> Expr:
    return self.__equality()
  
  def parse(self) -> Expr:
    try:
      return self.__expression()
    except Parser.ParseError as error:
      return None
  
  def __equality(self) -> Expr:
    expr: Expr = self.__comparison()
    
    while self.__match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
      operator: Token = self.__previous()
      right: Expr = self.__comparison()
      expr = Binary(expr, operator, right)
    
    return expr
  
  def __comparison(self) -> Expr:
    expr: Expr = self.__term()
    
    while self.__match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
      operator: Token = self.__previous()
      right: Expr = self.__term()
      expr = Binary(expr, operator, right)
      
    return expr
  
  def __term(self) -> Expr:
    expr: Expr = self.__factor()
    
    while self.__match(TokenType.MINUS, TokenType.PLUS):
      operator: Token = self.__previous()
      right: Token = self.__factor()
      expr = Binary(expr, operator, right)
      
    return expr
  
  def __factor(self) -> Expr:
    expr: Expr = self.__unary()
    
    while self.__match(TokenType.SLASH, TokenType.STAR):
      operator: Token = self.__previous()
      right: Token = self.__unary()
      expr = Binary(expr, operator, right)
      
    return expr
  
  def __unary(self) -> Expr:
    if self.__match(TokenType.BANG, TokenType.MINUS):
      operator: Token = self.__previous()
      right: Token = self.__unary()
      return Unary(operator, right)
      
    return self.__primary()
  
  def __primary(self) -> Expr:
    if self.__match(TokenType.FALSE): return Literal(False)
    if self.__match(TokenType.TRUE): return Literal(True)
    if self.__match(TokenType.NIL): return Literal(None)
    
    if self.__match(TokenType.NUMBER, TokenType.STRING):
      return Literal(self.__previous().literal)
    
    if self.__match(TokenType.LEFT_PAREN):
      expr: Expr = self.__expression()
      self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)
    
    raise self.__error(self.__peek(), "Expect expression.")
    
  def __consume(self, type:TokenType, message:str) -> Token:
    if self.__match(type): return self.__advance()
    
    raise self.__error(self.__peek(), message)
  
  def __error(self, token:Token, message:str) -> "Parser.ParseError":
    from Lox import Lox
    Lox.errort(token, message)
    return Parser.ParseError()
  
  def __match(self, *types: TokenType) -> bool:
    for type in types:
      if self.__check(type):
        self.__advance()
        return True
      
    return False
  
  def __check(self, type: TokenType) -> bool:
    if self.__isAtEnd():
      return False
    
    return self.__peek().type == type
  
  def __isAtEnd(self) -> bool:
    return self.__peek().type == TokenType.EOF
  
  def __advance(self) -> Token:
    if(not self.__isAtEnd()):
      self.current += 1
    
    return self.__previous()
  
  def __peek(self) -> Token:
    return self.tokens[self.current]
  
  def __previous(self) -> Token:
    return self.tokens[self.current - 1]
  
  def __synchronize(self) -> None:
    self.__advance()

    while not self.__isAtEnd():
      if self.__previous().type == TokenType.SEMICOLON:
        return

      if self.__peek().type in {
        TokenType.CLASS,
        TokenType.FUN, 
        TokenType.VAR,
        TokenType.FOR, 
        TokenType.IF, 
        TokenType.WHILE,
        TokenType.PRINT, 
        TokenType.RETURN
      }:
        return

      self.__advance()

  