from sys import argv, exit
from Lox import Lox

def main():
  print("Welcome to Ploxy!")
  if len(argv) > 1:
    print("Usage: lox [script]")
    exit(64)
  elif len(argv) == 2:
    Lox.runFile(argv[1])
  else:
    Lox.runPrompt()
    
    
if __name__ == "__main__":
    main()