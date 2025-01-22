import sys
from Scanner import Scanner

class Lox:
  had_error: bool = False
  
  @staticmethod
  def runFile(path):
    with open(path, "r", encoding="utf-8") as file:
        contents = file.read()
    Lox.__run(contents)
    
    if had_error:
      sys.exit(65)
    
  @staticmethod
  def runPrompt():
    global had_error
    while True:
      line = input(">> ")
      if line is None:
        break
      Lox.__run(line)
      
      had_error = False
      
  @staticmethod
  def __run(source):
    scanner = Scanner(source)
    tokens = scanner.scanTokens()
    # For now, just print the tokens.
    for token in tokens:
        print(token)
    
  @staticmethod
  def error(line, message):
    Lox.__report(line, "", message)
    
  @staticmethod
  def __report(line, where, message):
    global had_error
    print(f"[line {line}] Error {where}: {message}", file = sys.stderr)
    had_error = True
    