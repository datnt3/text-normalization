import re
from ctnx import num_to_words

from core.n2w_handler.converter.base import BaseNSWConverter

class DateConverter(BaseNSWConverter):
  def convert(self, category: str, value: str) -> str:
    if category == "dmdmy":
      return self.dmdmy_convert(value)
    if category == "ddmy":
      return self.ddmy_convert(value)
    if category == "dmdm":
      return self.dmdm_convert(value)
    if category == "dmydmy":
      return self.dmydmy_convert(value)
    if category == "mymy":
      return self.mymy_convert(value)
    if category == "dmy":
      return self.dmy_convert(value)
    if category == "mmy":
      return self.mmy_convert(value)
    if category == "qqy":
      return self.qqy_convert(value)
    if category == "ddm":
      return self.ddm_convert(value)
    if category == "qq":
      return self.qq_convert(value)
    if category == "dd":
      return self.dd_convert(value)
    if category == "mm":
      return self.mm_convert(value)
    if category == "yy":
      return self.yy_convert(value)
    if category == "my":
      return self.my_convert(value)
    if category == "dm":
      return self.dm_convert(value)
    if category == "qy":
      return self.qy_convert(value)
    
  def dmdmy_convert(self, value: str) -> str:
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
  
  def ddmy_convert(self, value: str) -> str:
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
      if i == 0:
        if prefix_match:
            prefix = prefix_match.group(1) + " "
            value_part = parts[i][prefix_match.end():]  
            day = value_part 
            if prefix == "ngày ":
              spoken_words.append(f"{prefix}{num_to_words(day)}")
            else:
              spoken_words.append(f"{prefix}ngày {num_to_words(day)}")
        else:
            value_part = parts[i]
            day = value_part
            spoken_words.append(f"ngày {num_to_words(day)}")
      else:
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
  
  def dmdm_convert(self, value: str) -> str:
    spoken_words = []

    value = value.strip()
    parts = re.split(r"[-–—−]", value)
    if len(parts) != 2:
      print("Wrong format")
      return value

    for i in range(len(parts)):
      parts[i] = parts[i].strip()
      prefix_match = re.match(r"^(ngày)\s*", parts[i])
      prefix = ""
      if prefix_match:
          prefix = prefix_match.group(1) + " "
          value_part = parts[i][prefix_match.end():]  
          day, month = re.split(r"[\.\/]", value_part)
          spoken_words.append(f"{prefix}{num_to_words(day)} tháng {num_to_words(month)}")
      else:
          value_part = parts[i]
          day, month = re.split(r"[\.\/]", value_part)
          spoken_words.append(f"ngày {num_to_words(day)} tháng {num_to_words(month)}")
    
    return " đến ".join(spoken_words)
    
  def dmydmy_convert(self, value: str) -> str:
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
  
  def mymy_convert(self, value: str) -> str:
    spoken_words = []

    value = value.strip()
    parts = re.split(r"[-–—−]", value)
    if len(parts) != 2:
      print("Wrong format")
      return value

    for i in range(len(parts)):
      parts[i] = parts[i].strip()
      prefix_match = re.match(r"^(tháng)\s*", parts[i])
      prefix = ""
      if prefix_match:
          prefix = prefix_match.group(1) + " "
          value_part = parts[i][prefix_match.end():]  
          month, year = re.split(r"[\.\/]", value_part)
          spoken_words.append(f"{prefix}{num_to_words(month)} năm {num_to_words(year)}")
      else:
          value_part = parts[i]
          month, year = re.split(r"[\.\/]", value_part)
          spoken_words.append(f"tháng {num_to_words(month)} năm {num_to_words(year)}")
    
    return " đến ".join(spoken_words)
  
  def dmy_convert(self, value: str) -> str:
    pass
  
  def mmy_convert(self, value: str) -> str:
    pass
  
  def qqy_convert(self, value: str) -> str:
    pass
  
  def ddm_convert(self, value: str) -> str:
    pass
  
  def qq_convert(self, value: str) -> str:
    pass
  
  def dd_convert(self, value: str) -> str:
    pass
  
  def mm_convert(self, value: str) -> str:
    pass
  
  def yy_convert(self, value: str) -> str:
    pass
  
  def my_convert(self, value: str) -> str:
    pass
  
  def dm_convert(self, value: str) -> str:
    pass
  
  def qy_convert(self, value: str) -> str:
    pass