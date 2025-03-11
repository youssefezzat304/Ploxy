import os
import sys

class GenerateAst:
  def __init__(self):
     pass
   
  @staticmethod
  def main(args: list[str]) -> None:
    if len(args) != 1:
      print("Usage: GenerateAst <output directory>", file=sys.stderr)
      sys.exit(64)

    outputDir: str = args[0]
    
    GenerateAst.__defineAst(outputDir, "Expr", [
    "Assign   : Token name, Expr value",
    "Binary   : Expr left, Token operator, Expr right",   
    "Call     : Expr callee, Token paren, list[Expr] arguments",  
    "Get      : Expr object, Token name",
    "Grouping : Expr expression",
    "Literal  : any value",
    "Logical  : Expr left, Token operator, Expr right",
    "Set      : Expr object, Token name, Expr value",
    "Super    : Token keyword, Token method",
    "This     : Token keyword",
    "Unary    : Token operator, Expr right",
    "Variable : Token name"
    ])
    
    GenerateAst.__defineAst(outputDir, "Stmt", [
      "Block : list[Stmt] statements",
      "Class : Token name, list['Function'] methods",
      "Expression : Expr expression",
      "Function : Token name, list[Token] params," + " list[Stmt] body",
      "If : Expr condition, Stmt thenBranch," +
      " Stmt elseBranch",
      "Print : Expr expression",
      "Return : Token keyword, Expr value",
      "Var : Token name, Expr initializer",
      "While : Expr condition, Stmt body"
    ])
    
  @staticmethod
  def __defineAst(outputDir: str, baseName: str, types: list[str]) -> None:
    path = os.path.join(outputDir, f"{baseName}.py")

    with open(path, "w", encoding="utf-8") as writer:
        writer.write("# This file is auto-generated by __defineAst.\n")
        writer.write("\n")
        writer.write("from typing import Protocol, TypeVar\n")
        writer.write("from Token import Token\n")
        writer.write("from abc import ABC, abstractmethod\n")
        writer.write("\n")
        writer.write("R = TypeVar('R')\n\n")
        
        writer.write(f"class {baseName}(ABC):\n")
        GenerateAst.__defineVisitor(writer, baseName, types)
        writer.write("    @abstractmethod\n")
        writer.write("    def accept(self, visitor: 'Expr.Visitor[R]') -> R:\n")
        writer.write("        raise NotImplementedError()\n")
        writer.write("\n")

        for type in types:
          className: str = type.split(":")[0].strip()
          fields = type.split(":")[1].strip()
          GenerateAst.__defineType(writer, baseName, className, fields)
                    
  @staticmethod
  def __defineType(writer, baseName: str, className: str, fieldList: str) -> None:
    writer.write(f"class {className}({baseName}):\n")
    fields = [field.strip() for field in fieldList.split(", ")] 
    constructor_args = ", ".join([f"{field.split(' ')[1]}: {field.split(' ')[0]}" for field in fields])
          
    writer.write(f"    def __init__(self, {constructor_args}) -> None:\n")

    for field in fields:
      name = field.split(" ")[1]
      writer.write(f"        self.{name} = {name}\n")
    writer.write("\n")
    
    writer.write("    def accept(self, visitor) -> R:\n")
    writer.write(f"        return visitor.visit{className}{baseName}(self)\n")
    writer.write("\n")
  
  @staticmethod
  def __defineVisitor(writer, baseName: str, types: list[str]) -> None:
    writer.write("    class Visitor(Protocol[R]):\n")
    
    for type in types:
      typeName: str = type.split(":")[0].strip()
      writer.write("       @abstractmethod\n")
      writer.write(f"       def visit{typeName}{baseName}(self, {baseName.lower()}: 'Expr.{typeName}'):\n")
      writer.write("          pass\n")
      
    writer.write("\n")
    
    
    
if __name__ == "__main__":
    GenerateAst.main(sys.argv[1:])