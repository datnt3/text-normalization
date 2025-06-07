import re
from typing import List
from core.data_preprocessing.data_augmentation.number_generator.base import (
    BaseGenerator,
)
from core.data_preprocessing.data_augmentation.number_rand import NumberRand

NUM_GEN = 5

class TelGenerator(BaseGenerator):
    def generate(self, category: str, value: str) -> List[str]:
      if category == "tel":
        return self.tel_generate(value)
    
    def tel_generate(self, value: str) -> List[str]:
      generated_list = []

      value = value.strip()
      value = re.sub(r"[^\d+]", "", value)
      
      for _ in range(NUM_GEN):
        tel_digits = NumberRand.tel_rand()
        value = f"{value[:(len(value) - 4)]}{tel_digits}"
        
        generated_list.append(value)

      return generated_list
      
