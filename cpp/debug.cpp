#include "debug.hpp"

void Disassembler::disassembleChunk(Chunk &chunk, const std::string &name)
{
  std::cout << "== " << name << " ==\n";
  const std::vector<uint8_t> &code = chunk.getCode();
  int offset = 0;
  while (offset < code.size())
  {
    offset = disassembleInstruction(chunk, offset);
  }
}

int Disassembler::disassembleInstruction(Chunk &chunk, int offset)
{
  const std::vector<uint8_t> &code = chunk.getCode();
  const std::vector<int> &lines = chunk.getLines();

  std::cout << std::setw(4) << std::setfill('0') << offset << " ";
  std::cout << std::setfill(' ');

  if (offset > 0 && lines[offset] == lines[offset - 1])
  {
    std::cout << "   | ";
  }
  else
  {
    std::cout << std::setw(4) << lines[offset] << " ";
  }

  uint8_t instruction = code[offset];
  switch (instruction)
  {
  case OP_CONSTANT:
    return constantInstruction("OP_CONSTANT", chunk, offset);
  case OP_ADD:
    return simpleInstruction("OP_ADD", offset);
  case OP_SUBTRACT:
    return simpleInstruction("OP_SUBTRACT", offset);
  case OP_MULTIPLY:
    return simpleInstruction("OP_MULTIPLY", offset);
  case OP_DIVIDE:
    return simpleInstruction("OP_DIVIDE", offset);
  case OP_NEGATE:
    return simpleInstruction("OP_NEGATE", offset);
  case OP_RETURN:
    return simpleInstruction("OP_RETURN", offset);
  default:
    std::cout << "Unknown opcode: " << static_cast<int>(instruction) << "\n";
    return offset + 1;
  }
}

int Disassembler::simpleInstruction(const std::string &name, int offset)
{
  std::cout << name << "\n";
  return offset + 1;
}

int Disassembler::constantInstruction(const std::string &name, Chunk &chunk, int offset)
{
  uint8_t constant = chunk.getCode()[offset + 1];
  std::cout << std::left << name << std::right << static_cast<int>(constant) << " '";

  printValue(chunk.getConstants().getValue(constant));
  std::cout << "'\n";

  return offset + 2;
}