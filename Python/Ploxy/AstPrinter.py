from Expr import Expr

class AstPrinter(Expr.Visitor[str]):
       
  def print(self, expr: Expr) -> str:
    return expr.accept(self)
  
  def visitBinaryExpr(self, expr: Expr.Binary) -> str:
    return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)
 
  def visitGroupingExpr(self, expr: Expr.Grouping) -> str:
    return self.__parenthesize("group", expr.expression)
 
  def visitLiteralExpr(self, expr: Expr.Literal) -> str:
    if (expr.value == None): 
      return "nil"
    
    return str(expr.value)
 
  def visitUnaryExpr(self, expr: Expr.Unary) -> str:
    return self.__parenthesize(expr.operator.lexeme, expr.right)

  def __parenthesize(self, name: str, *exprs: 'Expr.Expr') -> str:
    builder = []
    builder.append(f"({name}")
    for  expr in exprs:
      builder.append(" ")
      builder.append(expr.accept(self))

    builder.append(")")
    return "".join(builder)

if __name__ == "__main__":
    AstPrinter().main([])
