import re
from ctnx import num_to_words

from core.n2w_handler.converter.base import BaseNSWConverter

class DateConverter(BaseNSWConverter):
  def convert(self, type: str, value: str) -> str:
    if type == "dmdmy":
      return self.dmdmy_convert(value=value)
    if type == "ddmy":
      return self.ddmy_convert(value=value)
    if type == "dmdm":
      return self.dmdm_convert(value=value)
    if type == "dmydmy":
      return self.dmydmy_convert(value=value)
    if type == "mymy":
      return self.mymy_convert(value=value)
    if type == "dmy":
      return self.dmy_convert(value=value)
    if type == "mmy":
      return self.mmy_convert(value=value)
    if type == "qqy":
      return self.qqy_convert(value=value)
    if type == "ddm":
      return self.ddm_convert(value=value)
    if type == "qq":
      return self.qq_convert(value=value)
    if type == "dd":
      return self.dd_convert(value=value)
    if type == "mm":
      return self.mm_convert(value=value)
    if type == "yy":
      return self.yy_convert(value=value)
    if type == "my":
      return self.my_convert(value=value)
    if type == "dm":
      return self.dm_convert(value=value)
    if type == "qy":
      return self.qy_convert(value=value)
    
  def dmdmy_convert(value: str) -> str:
    spoken_words = []

    value = value.strip()
    parts = re.split(r"[-–—−]", value)
    if len(parts) != 2:
      print("Wrong format")
      return value

    for i in range(len(parts)):
      parts[i] = parts[i].strip()
      prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", parts[i])
      prefix = ""
      if prefix_match:
          prefix = prefix_match.group(1) + " "
          value_part = parts[i][prefix_match.end():]  
          splitted_value_part = re.split(r"[\.\/]", value_part)
          if len(splitted_value_part) == 2:
            day = splitted_value_part[0]
            month = splitted_value_part[1]
            if prefix == "ngày ":
              spoken_words.append(f"{prefix}{num_to_words(day)} tháng {num_to_words(month)}")
            else:
              spoken_words.append(f"{prefix}ngày {num_to_words(day)} tháng {num_to_words(month)}")
          elif len(splitted_value_part) == 3:
            day = splitted_value_part[0]
            month = splitted_value_part[1]
            year = splitted_value_part[2]
            if prefix == "ngày ":
              spoken_words.append(f"{prefix}{num_to_words(day)} tháng {num_to_words(month)} năm {num_to_words(year)}")
            else:
              spoken_words.append(f"{prefix}ngày {num_to_words(day)} tháng {num_to_words(month)} năm {num_to_words(year)}")
      else:
          value_part = parts[i]
          splitted_value_part = re.split(r"[\.\/]", value_part)
          if len(splitted_value_part) == 2:
            day = splitted_value_part[0]
            month = splitted_value_part[1]
            spoken_words.append(f"ngày {num_to_words(day)} tháng {num_to_words(month)}")
          elif len(splitted_value_part) == 3:
            day = splitted_value_part[0]
            month = splitted_value_part[1]
            year = splitted_value_part[2]
            spoken_words.append(f"ngày {num_to_words(day)} tháng {num_to_words(month)} năm {num_to_words(year)}")
            
    return " đến ".join(spoken_words) 
  
  def ddmy_convert(value: str) -> str:
    
    pass
  
  def dmdm_convert(value: str) -> str:
    pass
  
  def dmydmy_convert(value: str) -> str:
    spoken_words = []

    value = value.strip()
    parts = re.split(r"[-–—−]", value)
    if len(parts) != 2:
      print("Wrong format")
      return value

    for i in range(len(parts)):
      parts[i] = parts[i].strip()
      prefix_match = re.match(r"^(ngày|sáng|trưa|chiều|tối)\s*", parts[i])
      prefix = ""
      if prefix_match:
          prefix = prefix_match.group(1) + " "
          value_part = parts[i][prefix_match.end():]  
          day, month, year = re.split(r"[\.\/]", value_part)
          if prefix == "ngày ":
            spoken_words.append(f"{prefix}{num_to_words(day)} tháng {num_to_words(month)} năm {num_to_words(year)}")
          else:
            spoken_words.append(f"{prefix}ngày {num_to_words(day)} tháng {num_to_words(month)} năm {num_to_words(year)}")
      else:
          value_part = parts[i]
          day, month, year = re.split(r"[\.\/]", value_part)
          spoken_words.append(f"ngày {num_to_words(day)} tháng {num_to_words(month)} năm {num_to_words(year)}")
    
    return " đến ".join(spoken_words) 
  
  def mymy_convert(value: str) -> str:
    
    pass
  
  def dmy_convert(value: str) -> str:
    pass
  
  def mmy_convert(value: str) -> str:
    pass
  
  def qqy_convert(value: str) -> str:
    pass
  
  def ddm_convert(value: str) -> str:
    pass
  
  def qq_convert(value: str) -> str:
    pass
  
  def dd_convert(value: str) -> str:
    pass
  
  def mm_convert(value: str) -> str:
    pass
  
  def yy_convert(value: str) -> str:
    pass
  
  def my_convert(value: str) -> str:
    pass
  
  def dm_convert(value: str) -> str:
    pass
  
  def qy_convert(value: str) -> str:
    pass