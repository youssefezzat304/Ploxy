#include <stdio.h>
#include "common.hpp"
#include "compiler.hpp"
#include "scanner.hpp"

void compile(const std::string *source)
{
  Scanner scanner(*source);

  int line = -1;

  while (true)
  {
    Token token = scanner.scanToken();

    if (token.line != line)
    {
      std::cout << token.line << " ";
      line = token.line;
    }
    else
    {
      std::cout << " | ";
    }

    std::cout << static_cast<int>(token.type) << " '" << token.lexeme << "'\n";

    if (token.type == TokenType::TOKEN_EOF)
      break;
  }
}