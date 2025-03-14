#ifndef clox_chunk_hpp
#define clox_chunk_hpp

#include "common.hpp"
#include "value.hpp"
#include <vector>

enum class OpCode
{
  OP_CONSTANT,
  OP_RETURN,
};

class Chunk
{
public:
  void writeChunk(uint8_t byte, int line);
  int addConstant(Value value);
  const std::vector<uint8_t> &getCode() const;
  const std::vector<int> &getLines() const;
  const ValueArray &getConstants() const;
  void clear();

private:
  std::vector<uint8_t> code;
  std::vector<int> lines;
  ValueArray constants;
};

#endif