#include <stdio.h>

#include "value.hpp"

void ValueArray::writeValue(Value value)
{
  return values.push_back(value);
}

int ValueArray::getCapacity() const
{
  return values.capacity();
}

int ValueArray::getCount() const
{
  return values.size();
}

Value ValueArray::getValue(int index) const
{
  return values[index];
}

void ValueArray::printValues() const
{
  for (const auto &value : values)
  {
    std::cout << value << " ";
  }
  std::cout << "\n";
}

void ValueArray::clear()
{
  values.clear();
}

void printValue(Value value)
{
  std::cout << value;
}