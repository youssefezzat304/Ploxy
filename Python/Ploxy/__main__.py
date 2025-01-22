from sys import argv, exit
from Ploxy import Lox

def main():
  print("Welcome to Ploxy!")
  if len(argv) > 1:
    print("Usage: jlox [script]")
    exit(64)
  elif len(argv) == 2:
    Lox.runFile(argv[1])
  else:
    Lox.runPrompt()
    
    
if __name__ == "__main__":
    main()