from .Token import Token
from .Expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call, Get, Set, This, Super
from .TokenType import TokenType
from .Stmt import Stmt, Expression, Print, Var, Block, If, While, Function, Return, Class

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
  
  def __function(self, kind: str) -> Function:
    name: Token = self.__consume(TokenType.IDENTIFIER, f"Expect {kind} name.")
    self.__consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
    parameters: list[Token] = []
    if not self.__check(TokenType.RIGHT_PAREN):
      while True:
        if len(parameters) >= 255:
          self.__error(self.__peek(), "Can't have more than 255 parameters.")
        
        parameters.append(self.__consume(TokenType.IDENTIFIER, "Expect parameter name."))
        
        if not self.__match(TokenType.COMMA):
          break
        
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")
    
    self.__consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
    body: list[Stmt] = self.__block()
    return Function(name, parameters, body)
  
  def __assignment(self) -> Expr:
    expr: Expr = self.__or()
    
    if self.__match(TokenType.EQUAL):
      equals: Token = self.__previous()
      value: Expr = self.__assignment()
      
      if isinstance(expr, Variable):
        name: Token = expr.name
        return Assign(name, value)
      elif isinstance(expr, Get):
        get: Get = expr
        return Set(get.object, get.name, value)
      
      self.__error(equals, "Invalid assignment target.")
    
    return expr
  
  def __or(self) -> Expr:
    expr: Expr = self.__and()
    
    while self.__match(TokenType.OR):
      operator: Token = self.__previous()
      right: Expr = self.__and()
      expr = Logical(expr, operator, right)
      
    return expr
  
  def __and(self) -> Expr:
    expr: Expr = self.__equality()
    
    while self.__match(TokenType.AND):
      operator: Token = self.__previous()
      right: Expr = self.__equality()
      expr = Logical(expr, operator, right)
      
    return expr
  
  def __decleration(self) -> Stmt:
    try:
      if self.__match(TokenType.CLASS): return self.__classDeclaration()
      if self.__match(TokenType.FUN): return self.__function("function")
      if self.__match(TokenType.VAR): return self.__varDeclaration()
      
      return self.__statment()
    except self.ParseError:
      self.__synchronize()
      
      return None
    
  def __classDeclaration(self) -> Stmt:
    name: Token = self.__consume(TokenType.IDENTIFIER, "Expect class name.")
    
    superclass: Variable = None
    if self.__match(TokenType.LESS):
      self.__consume(TokenType.IDENTIFIER, "Expect superclass name.")
      superclass = Variable(self.__previous())
      
    self.__consume(TokenType.LEFT_BRACE, "Expect '{' before class body.")
    
    methods: list[Function] = []
    while not self.__check(TokenType.RIGHT_BRACE) and not self.__isAtEnd():
      methods.append(self.__function("method"))
      
    self.__consume(TokenType.RIGHT_BRACE, "Expect '}' after class body.")
    
    return Class(name, superclass, methods)
    
  def __varDeclaration(self) -> Stmt:
    name: Token = self.__consume(TokenType.IDENTIFIER, "Expect variable name.")
    
    initializer: Expr = None
    if self.__match(TokenType.EQUAL):
      initializer = self.__expression()
      
    self.__consume(TokenType.SEMICOLON, "Expect ';' after value.")
    return Var(name, initializer)
  
  def __whileStatment(self) -> Stmt:
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
    condition: Expr = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
    body: Stmt = self.__statment()
    
    return While(condition, body)
  
  def __statment(self) -> Stmt:
    if self.__match(TokenType.FOR):
      return self.__forStatment()
    
    if self.__match(TokenType.IF):
      return self.__ifStatment()
    
    if self.__match(TokenType.PRINT):
      return self.__printStatment()
    
    if self.__match(TokenType.RETURN):
      return self.__returnStatment()
    
    if self.__match(TokenType.WHILE):
      return self.__whileStatment()
    
    if self.__match(TokenType.LEFT_BRACE):
      return Block(self.__block())
    
    return self.__expressionStatment()
  
  def __forStatment(self) -> Stmt:
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")
    
    initializer: Stmt
    if self.__match(TokenType.SEMICOLON):
      initializer = None
    elif self.__match(TokenType.VAR):
      initializer = self.__varDeclaration()
    else:
      initializer = self.__expressionStatment()
    
    condition: Expr = None
    if not self.__check(TokenType.SEMICOLON):
      condition = self.__expression()
    self.__consume(TokenType.SEMICOLON, "Expect ';' after loop condion.")  
    
    increment: Expr = None
    if not self.__check(TokenType.RIGHT_PAREN):
      increment = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")
    body: Stmt = self.__statment()
    
    if increment != None:
      body = Block([body, Expression(increment)])
      
    if condition == None:
      condition = Literal(True)
    body = While(condition, body)
    
    if initializer != None:
      body = Block([initializer, body])
    
    return body
  
  def __ifStatment(self) -> Stmt:
    self.__consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
    condition: Expr = self.__expression()
    self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")
    
    thenBranch: Stmt = self.__statment()
    elseBranch: Stmt = None
    
    if self.__match(TokenType.ELSE):
      elseBranch = self.__statment()
      
    return If(condition, thenBranch, elseBranch)
  
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
  
  def __returnStatment(self) -> Stmt:
    keyword: Token = self.__previous()
    value: Expr = None
    if not self.__check(TokenType.SEMICOLON):
      value = self.__expression()
      
    self.__consume(TokenType.SEMICOLON, "Expect ';' after return value.")
    return Return(keyword, value)
  
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
      
    return self.__call()
  
  def __call(self) -> Expr:
    expr: Expr = self.__primary()
    
    while True:
      if self.__match(TokenType.LEFT_PAREN):
        expr = self.__finishCall(expr)
      elif self.__match(TokenType.DOT):
        name: Token = self.__consume(TokenType.IDENTIFIER, "Expect property name after '.'.")
        expr = Get(expr, name)
      else:
        break
      
    return expr
  
  def __finishCall(self, callee: Expr) -> Expr:
    arguments: list[Expr] = []
    
    if not self.__check(TokenType.RIGHT_PAREN):
      while True:
        if len(arguments) >= 255:
          self.__error(self.__peek(), "Can't have more than 255 arguments.")
        arguments.append(self.__expression())
        if not self.__match(TokenType.COMMA):
          break
    
    paren: Token = self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
    
    return Call(callee, paren, arguments)
  
  def __primary(self) -> Expr:
    if self.__match(TokenType.FALSE): return Literal(False)
    if self.__match(TokenType.TRUE): return Literal(True)
    if self.__match(TokenType.NIL): return Literal(None)
    
    if self.__match(TokenType.NUMBER, TokenType.STRING):
      return Literal(self.__previous().literal)
    
    if self.__match(TokenType.SUPER):
      keyword: Token = self.__previous()
      self.__consume(TokenType.DOT, "Expect '.' after 'super'.")
      method: Token = self.__consume(TokenType.IDENTIFIER, "Expect superclass method name.")
      return Super(keyword, method)
    
    if self.__match(TokenType.THIS): return This(self.__previous())
    
    if self.__match(TokenType.IDENTIFIER):
      return Variable(self.__previous())
    
    if self.__match(TokenType.LEFT_PAREN):
      expr: Expr = self.__expression()
      self.__consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
      return Grouping(expr)
    
    raise self.__error(self.__peek(), "Expect expression.")
    
  def __consume(self, type: TokenType, message:str) -> Token:
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

  