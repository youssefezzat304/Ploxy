#ifndef clox_debug_hpp
#define clox_debug_hpp

#include "chunk.hpp"
#include <iostream>
#include <iomanip>

class Disassembler
{
public:
  void disassembleChunk(const Chunk &chunk, const std::string &name);
  int disassembleInstruction(const Chunk &chunk, int offset);
  static int simpleInstruction(const std::string &name, int offset);
  static int constantInstruction(const std::string &name, const Chunk &chunk, int offset);
};

#endif