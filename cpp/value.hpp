#ifndef clox_value_hpp
#define clox_value_hpp

#include "common.hpp"
#include <vector>
#include <iostream>

using Value = double;

class ValueArray
{
public:
  ValueArray() = default;

  void writeValue(Value value);
  void printValues() const;
  void clear();
  int getCapacity() const;
  int getCount() const;
  Value getValue(int index) const;

private:
  std::vector<Value> values;
};

void printValue(Value value);

#endif