from abc import ABC, abstractmethod

class BaseInference(ABC):
  @abstractmethod
  def infer_all(self):
    """
    Abstract method to perform inference on all data.
    Should be implemented by subclasses.
    """
    pass
  @abstractmethod
  def infer_one(self, input: str):
    """
    Abstract method to perform inference on a single input.
    Should be implemented by subclasses.
    
    Args:
        input (str): The input string to infer.
        
    Returns:
        str: The predicted label for the input.
    """
    pass
  
  