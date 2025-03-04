from Token import Token
from Expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign
from TokenType import TokenType
from Stmt import Stmt, Expression, Print, Var, Block

class Parser:
  class ParseError(Exception):
    pass
  
  def __init__(self, tokens: list[Token]):
    self.tokens: list[Token] = tokens
    self.current: int = 0
        
  def parse(self) -> list[Stmt]:
    statments: list[Stmt] = []

    while not self.__isAtEnd():
      statments.append(self.__decleration())
    
    return statments
  
  def __expression(self) -> Expr:
    return self.__assignment()
  
  def __assignment(self) -> Expr:
    expr: Expr = self.__equality()
    
    if self.__match(TokenType.EQUAL):
      equals: Token = self.__previous()
      value: Expr = self.__assignment()
      
      if isinstance(expr, Variable):
        name: Token = expr.name
        return Assign(name, value)
      
      self.__error(equals, "Invalid assignment target.")
    
    return expr
  
  def __decleration(self) -> Stmt:
    try:
      if self.__match(TokenType.VAR): return self.__varDeclaration()
      
      return self.__statment()
    except self.ParseError:
      self.__synchronize()
      
      return None
    
  def __varDeclaration(self) -> Stmt:
    name: Token = self.__consume(TokenType.IDENTIFIER, "Expect variable name.")
    
    initializer: Expr = None
    if self.__match(TokenType.EQUAL):
      initializer = self.__expression()
      
    self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
    return Var(name, initializer)
  
  def __statment(self) -> Stmt:
    if self.__match(TokenType.PRINT):
      return self.__printStatment()
    if self.__match(TokenType.LEFT_BRACE):
      return Block(self.__block())
    
    return self.__expressionStatment()
  
  def __block(self) -> list[Stmt]:
    statments: list[Stmt] = []
    
    while not self.__check(TokenType.RIGHT_BRACE) and not self.__isAtEnd():
      statments.append(self.__decleration())
      
    self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
    return statments
  
  def __printStatment(self) -> Stmt:
    value: Expr = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
    return Print(value)
  
  def __expressionStatment(self) -> Stmt:
    expr: Expr = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after expression")
    return Expression(expr)
  
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
    
    if self.__match(TokenType.IDENTIFIER):
      return Variable(self.__previous())
    
    if self.__match(TokenType.LEFT_PAREN):
      expr: Expr = self.__expression()
      self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)
    
    raise self.__error(self.__peek(), "Expect expression.")
    
  def __consume(self, type:TokenType, message:str) -> Token:
    if self.__check(type):
      return self.__advance()
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
    if not self.__isAtEnd():
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

  