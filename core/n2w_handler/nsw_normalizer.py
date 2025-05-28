from core.n2w_handler.converter.date import DateConverter
from core.n2w_handler.converter.time import TimeConverter
from core.n2w_handler.converter.tel import TelConverter



class NSWNormalizer():
  def __init__(self):
    self.registry = {}

    date_categories = [
      "dmdmy",
      "ddmy",
      "dmdm",
      "dmydmy",
      "mymy",
      "dmy",
      "mmy",
      "qqy",
      "ddm",
      "qq",
      "dd",
      "mm",
      "yy",
      "my",
      "dm",
      "qy",
    ]
    
    time_categories = [
      "hmshms",
      "hmhm",
      "msms",
      "hms",
      "hh",
      "t_mm",
      "ss",
      "hm",
      "ms",
      "hour",
    ]
    
    tel_categories = [
      "tel"
    ]
    
    converters = [
      (date_categories, DateConverter()),
      (time_categories, TimeConverter()),
      (tel_categories, TelConverter()),
    ]
    
    for categories, converter in converters:
      for category in categories:
        self.registry[category] = converter
      
  def convert(self, category: str, value: str):
    converter = self.registry.get(category)
    if converter:
      spoken_word = converter.convert(category=category, value=value)
      return spoken_word
    return value