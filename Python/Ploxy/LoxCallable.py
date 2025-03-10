from abc import ABC, abstractmethod
from typing import List, Any

class LoxCallable(ABC):
  def arity(self) -> int:
    pass
     
  @abstractmethod
  def call(self, interpreter, arguments: List[Any]) -> Any:
    pass
