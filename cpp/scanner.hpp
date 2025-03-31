#ifndef clox_scanner_hpp
#define clox_scanner_hpp

#include <string>

enum class TokenType
{
  TOKEN_LEFT_PAREN,
  TOKEN_RIGHT_PAREN,
  TOKEN_LEFT_BRACE,
  TOKEN_RIGHT_BRACE,
  TOKEN_COMMA,
  TOKEN_DOT,
  TOKEN_MINUS,
  TOKEN_PLUS,
  TOKEN_SEMICOLON,
  TOKEN_SLASH,
  TOKEN_STAR,

  TOKEN_BANG,
  TOKEN_BANG_EQUAL,
  TOKEN_EQUAL,
  TOKEN_EQUAL_EQUAL,
  TOKEN_GREATER,
  TOKEN_GREATER_EQUAL,
  TOKEN_LESS,
  TOKEN_LESS_EQUAL,

  TOKEN_IDENTIFIER,
  TOKEN_STRING,
  TOKEN_NUMBER,

  TOKEN_AND,
  TOKEN_CLASS,
  TOKEN_ELSE,
  TOKEN_FALSE,
  TOKEN_FOR,
  TOKEN_FUN,
  TOKEN_IF,
  TOKEN_NIL,
  TOKEN_OR,
  TOKEN_PRINT,
  TOKEN_RETURN,
  TOKEN_SUPER,
  TOKEN_THIS,
  TOKEN_TRUE,
  TOKEN_VAR,
  TOKEN_WHILE,

  TOKEN_ERROR,
  TOKEN_EOF
};

struct Token
{
  TokenType type;
  std::string lexeme;
  int line;

  Token(TokenType type, const std::string &lexeme, int line)
      : type(type), lexeme(lexeme), line(line) {}
};

class Scanner
{
public:
  explicit Scanner(const std::string &source);

  bool isAtEnd() const;
  Token makeToken(TokenType type);
  Token errorToken(const std::string &message);
  char advance();
  char peekNext() const;
  bool match(char expected);
  void skipWhitespace();
  char peek() const;
  Token string();
  bool isDigit(char c) const;
  Token number();
  bool isAlpha(char c) const;
  Token identifier();
  TokenType identifierType();
  TokenType checkKeyword(int startOffset, int length, const char *rest, TokenType type);

  Token scanToken();

private:
  std::string source;
  size_t start;
  size_t current;
  int line;
};

#endif