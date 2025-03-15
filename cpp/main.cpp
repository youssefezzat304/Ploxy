#include "common.hpp"
#include "chunk.hpp"
#include "debug.hpp"
#include "value.hpp"
#include "vm.hpp"

int main(int argc, const char *argv[])
{
  VM vm;
  Chunk chunk;
  int constant = chunk.addConstant(1.2);
  chunk.writeChunk(OP_CONSTANT, 123);
  chunk.writeChunk(constant, 123);
  constant = chunk.addConstant(3.4);
  chunk.writeChunk(OP_CONSTANT, 123);
  chunk.writeChunk(constant, 123);
  chunk.writeChunk(OP_ADD, 123);
  constant = chunk.addConstant(5.6);
  chunk.writeChunk(OP_CONSTANT, 123);
  chunk.writeChunk(constant, 123);
  chunk.writeChunk(OP_DIVIDE, 123);
  chunk.writeChunk(OP_NEGATE, 123);
  chunk.writeChunk(OP_RETURN, 123);

  Disassembler dis;
  dis.disassembleChunk(chunk, "test chunk");
  vm.interpret(&chunk);
  chunk.clear();
  return 0;
}