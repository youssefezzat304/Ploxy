#include "vm.hpp"
#include "common.hpp"
#include <iostream>

constexpr bool DEBUG_TRACE_EXECUTION = true;
void log(const std::string &message)
{
  std::cout << message << "\n";
}

InterpretResult VM::interpret(Chunk *chunk)
{
  this->chunk = chunk;
  this->ip = chunk->getCode().data();
  return run();
}

void VM::push(Value value)
{
  *stackTop = value;
  stackTop++;
}

Value VM::pop()
{
  stackTop--;
  return *stackTop;
}

uint8_t VM::readByte()
{
  return *ip++;
}

Value VM::readConstant()
{
  uint8_t constantIndex = readByte();
  return chunk->getConstants().getValue(constantIndex);
}

void VM::binary_op(char op)
{
  double b = pop();
  double a = pop();

  switch (op)
  {
  case '+':
    push(a + b);
    break;
  case '-':
    push(a - b);
    break;
  case '*':
    push(a * b);
    break;
  case '/':
    push(a / b);
    break;
  default:
    throw std::invalid_argument("Unknown operation");
  }
}

InterpretResult VM::run()
{
  while (true)
  {
    uint8_t instruction;
    if constexpr (DEBUG_TRACE_EXECUTION)
    {
      for (Value *slot = stack; slot < stackTop; slot++)
      {
        std::cout << "[ ";
        printValue(*slot);
        std::cout << " ]\n";
      }
      log("Executing instruction: " + std::to_string(static_cast<int>(instruction)));
      log("Instruction pointer: " + std::to_string(reinterpret_cast<uintptr_t>(ip)));
    }
    switch (instruction = readByte())
    {
    case OP_CONSTANT:
    {
      Value constant = readConstant();
      push(constant);
      break;
    }
    case OP_ADD:
    {
      binary_op('+');
      break;
    }
    case OP_SUBTRACT:
    {
      binary_op('-');
      break;
    }
    case OP_MULTIPLY:
    {
      binary_op('*');
      break;
    }
    case OP_DIVIDE:
    {
      binary_op('/');
      break;
    }
    case OP_NEGATE:
    {
      push(-pop());
      break;
    }
    case OP_RETURN:
    {
      printValue(pop());
      std::cout << "\n";
      return INTERPRET_OK;
    }
    default:
    {
      if constexpr (DEBUG_TRACE_EXECUTION)
      {
        log("Unknown opcode: " + std::to_string(static_cast<int>(instruction)));
      }
      break;
    }
    }
  }
}
