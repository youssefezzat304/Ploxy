#include <stdio.h>
#include <string.h>
#include "common.hpp"
#include "scanner.hpp"
#include <unordered_map>

Scanner::Scanner(const std::string &source) : source(source), start(0), current(0), line(1) {}

bool Scanner::isDigit(char c) const
{
  return c >= '0' && c <= '9';
}

bool Scanner::isAlpha(char c) const
{
  return (c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_';
}

Token Scanner::identifier()
{
  while (isAlpha(peek()) || isDigit(peek()))
    advance();

  return makeToken(TokenType::TOKEN_IDENTIFIER);
}

Token Scanner::number()
{
  while (isDigit(peek()))
    advance();

  if (peek() == '.' && isDigit(peekNext()))
  {
    advance();
    while (isDigit(peek()))
      advance();
  }

  return makeToken(TokenType::TOKEN_NUMBER);
}

Token Scanner::scanToken()
{
  skipWhitespace();

  start = current;

  if (isAtEnd())
    return makeToken(TokenType::TOKEN_EOF);

  char c = advance();

  if (isAlpha(c))
    return identifier();
  if (isDigit(c))
    return number();

  switch (c)
  {
  case '(':
    return makeToken(TokenType::TOKEN_LEFT_PAREN);
  case ')':
    return makeToken(TokenType::TOKEN_RIGHT_PAREN);
  case '{':
    return makeToken(TokenType::TOKEN_LEFT_BRACE);
  case '}':
    return makeToken(TokenType::TOKEN_RIGHT_BRACE);
  case ';':
    return makeToken(TokenType::TOKEN_SEMICOLON);
  case ',':
    return makeToken(TokenType::TOKEN_COMMA);
  case '.':
    return makeToken(TokenType::TOKEN_DOT);
  case '-':
    return makeToken(TokenType::TOKEN_MINUS);
  case '+':
    return makeToken(TokenType::TOKEN_PLUS);
  case '*':
    return makeToken(TokenType::TOKEN_STAR);
  case '!':
    return makeToken(match('=') ? TokenType::TOKEN_BANG_EQUAL : TokenType::TOKEN_BANG);
  case '=':
    return makeToken(match('=') ? TokenType::TOKEN_EQUAL_EQUAL : TokenType::TOKEN_EQUAL);
  case '<':
    return makeToken(match('=') ? TokenType::TOKEN_LESS_EQUAL : TokenType::TOKEN_LESS);
  case '>':
    return makeToken(match('=') ? TokenType::TOKEN_GREATER_EQUAL : TokenType::TOKEN_GREATER);

  case '"':
    return string();
  case '/':
    if (peekNext() == '/')
    {
      while (peek() != '\n' && !isAtEnd())
        advance();
    }
    else
    {
      return;
    }
  default:
    return errorToken("Unexpected character.");
  }
}

bool Scanner::isAtEnd() const
{
  return current >= source.length();
}

Token Scanner::makeToken(TokenType type)
{
  std::string lexeme = source.substr(start, current - start);
  return Token(type, lexeme, line);
}

Token Scanner::errorToken(const std::string &message)
{
  return Token(TokenType::TOKEN_ERROR, message, line);
}

char Scanner::advance()
{
  return source[current++];
}

bool Scanner::match(char expected)
{
  if (isAtEnd())
    return false;
  if (source[current] != expected)
    return false;

  current++;
  return true;
}

void Scanner::skipWhitespace()
{
  while (true)
  {
    char c = peek();
    switch (c)
    {
    case ' ':
    case '\r':
    case '\t':
      advance();
      break;
    default:
      return;
    }
  }
}

TokenType Scanner::identifierType()
{
  char firstChar = source[start];
  switch (firstChar)
  {
  case 'a':
    return checkKeyword(1, 2, "nd", TokenType::TOKEN_AND);
  case 'c':
    return checkKeyword(1, 4, "lass", TokenType::TOKEN_CLASS);
  case 'e':
    return checkKeyword(1, 3, "lse", TokenType::TOKEN_ELSE);
  case 'i':
    return checkKeyword(1, 1, "f", TokenType::TOKEN_IF);
  case 'n':
    return checkKeyword(1, 2, "il", TokenType::TOKEN_NIL);
  case 'o':
    return checkKeyword(1, 1, "r", TokenType::TOKEN_OR);
  case 'p':
    return checkKeyword(1, 4, "rint", TokenType::TOKEN_PRINT);
  case 'r':
    return checkKeyword(1, 5, "eturn", TokenType::TOKEN_RETURN);
  case 's':
    return checkKeyword(1, 4, "uper", TokenType::TOKEN_SUPER);
  case 't':
    if (current - start > 1)
    {
      switch (source[start + 1])
      {
      case 'h':
        return checkKeyword(2, 2, "is", TokenType::TOKEN_THIS);
      case 'r':
        return checkKeyword(2, 2, "ue", TokenType::TOKEN_TRUE);
      }
    }
  case 'v':
    return checkKeyword(1, 2, "ar", TokenType::TOKEN_VAR);
  case 'w':
    return checkKeyword(1, 4, "hile", TokenType::TOKEN_WHILE);
  case 'f':
    if (current - start > 1)
    {
      switch (source[start + 1])
      {
      case 'a':
        return checkKeyword(2, 3, "lse", TokenType::TOKEN_FALSE);
      case 'o':
        return checkKeyword(2, 1, "r", TokenType::TOKEN_FOR);
      case 'u':
        return checkKeyword(2, 1, "n", TokenType::TOKEN_FUN);
      }
    }
  default:
    break;
  }
  return TokenType::TOKEN_IDENTIFIER;
}

TokenType Scanner::checkKeyword(int startOffset, int length, const char *rest, TokenType type)
{
  if (current - start == startOffset + length &&
      memcmp(source.c_str() + start + startOffset, rest, length) == 0)
  {
    return type;
  }

  return TokenType::TOKEN_IDENTIFIER;
}

Token Scanner::string()
{
  while (peek() != '"' && !isAtEnd())
  {
    if (peek() == '\n')
      advance();
  }

  if (isAtEnd())
    return errorToken("Unterminated string.");

  advance();

  return makeToken(TokenType::TOKEN_STRING);
}

char Scanner::peek() const
{
  if (isAtEnd())
    return '\0';
  return source[current];
}

char Scanner::peekNext() const
{
  if (isAtEnd())
    return '\0';
  return source[current + 1];
}

Scanner scanner;
