from abc import ABC, abstractmethod

class BaseNSWConverter(ABC):
  @abstractmethod
  def convert(self, category: str, value: str) -> str:
    """
    Converts a given NSW value based on its category.
    """
    pass