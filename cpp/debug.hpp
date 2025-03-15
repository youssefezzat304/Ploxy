#ifndef clox_debug_hpp
#define clox_debug_hpp

#include "chunk.hpp"
#include <iostream>
#include <iomanip>

class Disassembler
{
public:
  void disassembleChunk(Chunk &chunk, const std::string &name);
  int disassembleInstruction(Chunk &chunk, int offset);
  static int simpleInstruction(const std::string &name, int offset);
  static int constantInstruction(const std::string &name, Chunk &chunk, int offset);
};

#endif