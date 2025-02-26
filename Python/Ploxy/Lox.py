import sys
from Scanner import Scanner
from Token import Token
from TokenType import TokenType
from Parser import Parser
from Expr import Expr
from AstPrinter import AstPrinter
from RuntimeError import RuntimeException
from Interpreter import Interpreter

class Lox:
  interpreter: Interpreter = Interpreter()
  hadError: bool = False
  hadRuntimeError: bool = False
  
  @staticmethod
  def runFile(path: str) -> None:
    with open(path, "r", encoding="utf-8") as file:
        contents = file.read()
    Lox.__run(contents)
    
    if Lox.hadError:
      sys.exit(65)
    if Lox.hadRuntimeError:
      sys.exit(70)
    
  @staticmethod
  def runPrompt() -> None:
    while True:
      line: str = input(">> ")
      if line is None:
        break
      Lox.__run(line)
      
      Lox.hadError = False
      
  @staticmethod
  def __run(source: str) -> None:
    scanner: Scanner = Scanner(source)
    tokens: list[Token] = scanner.scanTokens()
    parser: Parser = Parser(tokens)
    expression: Expr = parser.parse()
    
    if Lox.hadError: return
    
    Lox.interpreter.interpret(expression)
    
  @staticmethod
  def runtimeError(error: RuntimeException) -> None:
    print(f"{error}\n[line {error.token.line}]", file=sys.stderr)
    Lox.hadRuntimeError = True
    
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
    print(f"[line {line}] Error {where}: {message}", file = sys.stderr)
    Lox.hadError = True
    