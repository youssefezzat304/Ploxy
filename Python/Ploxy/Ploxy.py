import sys
from Scanner import Scanner
from Token import Token
from TokenType import TokenType
from Parser import Parser
from Expr import Expr
from AstPrinter import AstPrinter

class Lox:
  had_error: bool = False
  
  @staticmethod
  def runFile(path: str) -> None:
    with open(path, "r", encoding="utf-8") as file:
        contents = file.read()
    Lox.__run(contents)
    
    if had_error:
      sys.exit(65)
    
  @staticmethod
  def runPrompt() -> None:
    global had_error
    while True:
      line: str = input(">> ")
      if line is None:
        break
      Lox.__run(line)
      
      had_error = False
      
  @staticmethod
  def __run(source: str) -> None:
    scanner: Scanner = Scanner(source)
    tokens: list[Token] = scanner.scanTokens()
    parser: Parser = Parser(tokens)
    expression: Expr = parser.parse()
    
    if had_error: return
    
    print(AstPrinter().print(expression))
    
  @staticmethod
  def errorl(line: int, message:str) -> None:
    Lox.__report(line, "", message)
    
  @staticmethod
  def errort(token:Token, message:str) -> None:
    if token.type == TokenType.EOF:
      Lox.__report(token.line, " at end", message)
    else:
      Lox.__report(token.line, f" at '{token.lexeme}'", message)
    
  @staticmethod
  def __report(line: int, where: str, message: str) -> None:
    global had_error
    print(f"[line {line}] Error {where}: {message}", file = sys.stderr)
    had_error = True
    