#ifndef clox_chunk_hpp
#define clox_chunk_hpp

#include "common.hpp"
#include "value.hpp"
#include <vector>

enum OpCode
{
  OP_CONSTANT,
  OP_ADD,
  OP_SUBTRACT,
  OP_MULTIPLY,
  OP_DIVIDE,
  OP_NEGATE,
  OP_RETURN,
};

class Chunk
{
public:
  void writeChunk(uint8_t byte, int line);
  int addConstant(Value value);
  std::vector<uint8_t> &getCode();
  const std::vector<int> &getLines() const;
  const ValueArray &getConstants() const;
  void clear();

private:
  std::vector<uint8_t> code;
  std::vector<int> lines;
  ValueArray constants;
};

#endif