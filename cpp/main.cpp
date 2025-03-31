#include <iostream>
#include "vm.hpp"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>

// Forward declaration
std::string readFile(const std::string &path);

void repl()
{
  VM vm;
  std::string line;
  while (true)
  {
    std::cout << "> ";

    if (!std::getline(std::cin, line))
    {
      std::cout << "\n";
      break;
    }
    
    vm.interpret(&line);
  }
}

static void runFile(const char *path)
{
  VM vm;
  vm.runFile(path);
}

int main(int argc, const char *argv[])
{
  VM vm;

  if (argc == 1)
  {
    repl();
  }
  else if (argc == 2)
  {
    runFile(argv[1]);
  }
  else
  {
    std::cerr << "Usage: clox [path]\n";
    return 64;
  }

  // Destructor for vm is automatically called here (replaces freeVM())
  return 0;
}