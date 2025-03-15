#ifndef clox_vm_hpp
#define clox_vm_hpp

#include "chunk.hpp"
#include "value.hpp"
#include <memory>

const int STACK_MAX = 256;

enum InterpretResult
{
  INTERPRET_OK,
  INTERPRET_COMPILE_ERROR,
  INTERPRET_RUNTIME_ERROR
};

class VM
{
public:
  VM() = default;

  InterpretResult interpret(Chunk *chunk);
  void push(Value value);
  Value pop();
  void binary_op(char op);

private:
  uint8_t readByte();
  Value readConstant();
  InterpretResult run();

  Chunk *chunk;
  uint8_t *ip;
  Value stack[STACK_MAX];
  Value *stackTop;
};

#endif
