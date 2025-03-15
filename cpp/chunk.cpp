#include "chunk.hpp"

void Chunk::writeChunk(uint8_t byte, int line)
{
  code.push_back(byte);
  lines.push_back(line);
}

void Chunk::clear()
{
  code.clear();
  lines.clear();
  constants.clear();
}

std::vector<uint8_t> &Chunk::getCode()
{
  return code;
}

const std::vector<int> &Chunk::getLines() const
{
  return lines;
}

const ValueArray &Chunk::getConstants() const
{
  return constants;
}

int Chunk::addConstant(Value value)
{
  constants.writeValue(value);
  return constants.getCount() - 1;
}
