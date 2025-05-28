from core.n2w_handler.converter.date import DateConverter


class NSWNormalizer():
  def __init__(self):
    self.registry = {}

    date_types = [
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
    
    time_types = [
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
    
    tel_types = [
      "tel"
    ]
    
    converters = [
      (date_types, DateConverter())
    ]
    
    for type, converter in converters:
      self.registry[type] = DateConverter()
      
  def convert(self, type: str, value: str):
    converter = self.registry.get(type)
    if converter:
      spoken_word = converter.convert(type=type, value=value)
      return spoken_word
    return value