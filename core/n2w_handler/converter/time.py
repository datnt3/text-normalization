import re
from ctnx import num_to_words
from vietnam_number import n2w_single

from core.n2w_handler.converter.base import BaseNSWConverter


class TimeConverter(BaseNSWConverter):
  def convert(self, category: str, value: str) -> str:
    if category == "hmhm":
      return self.hmhm_convert(value)
  
  def hmhm_convert(self, value: str) -> str:
    spoken_words = []

    value = value.strip()
    parts = re.split(r"[-–—−]", value)
    if len(parts) != 2:
      print("Wrong format")
      return value
    
    for i in range(len(parts)):
      parts[i] = parts[i].strip()
      hour, minute = re.split(r"[hg:]", parts[i])
      if int(minute) != 0:
        spoken_words.append(f"{num_to_words(hour)} giờ {num_to_words(minute)} phút")
      else:
        spoken_words.append(f"{num_to_words(hour)} giờ")
        
    return " đến ".join(spoken_words)
  
    