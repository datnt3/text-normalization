from abc import ABC, abstractmethod
from typing import List

class BaseGenerator(ABC):
  @abstractmethod
  def generate(self, category: str, value: str) -> List[str]:
    """
    Converts a given NSW value based on its category.
    """
    pass