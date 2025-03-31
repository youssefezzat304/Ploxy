from sys import argv, exit
from .Lox import Lox

def main():
    print("Welcome to Ploxy!")
    if len(argv) > 2:
        print("Usage: ploxy [command] [script]")
        exit(64)
    elif len(argv) == 2:
        if argv[1] == "run":
            Lox.runPrompt()
        else:
            Lox.runFile(argv[1])
    elif len(argv) == 3 and argv[1] == "run":
        Lox.runFile(argv[2])
    else:
        Lox.runPrompt()

if __name__ == "__main__":
    main()