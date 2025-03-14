#include "common.hpp"
#include "chunk.hpp"
#include "debug.hpp"
#include "value.hpp"

int main(int argc, const char *argv[])
{
  Chunk chunk;
  int constant = chunk.addConstant(1.2);
  chunk.writeChunk(static_cast<uint8_t>(OpCode::OP_CONSTANT), 123);
  chunk.writeChunk(constant, 123);
  chunk.writeChunk(static_cast<uint8_t>(OpCode::OP_RETURN), 123);

  Disassembler dis;
  dis.disassembleChunk(chunk, "test chunk");
  
  chunk.clear();
  return 0;
}