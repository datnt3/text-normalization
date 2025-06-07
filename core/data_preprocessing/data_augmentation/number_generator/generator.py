from core.data_preprocessing.data_augmentation.number_generator.date_generator import DateGenerator
from core.data_preprocessing.data_augmentation.number_generator.time_generator import TimeGenerator
from core.data_preprocessing.data_augmentation.number_generator.tel_generator import TelGenerator


class Generator():
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
    
    generators = [
      (date_categories, DateGenerator()),
      (time_categories, TimeGenerator()),
      (tel_categories, TelGenerator())
    ]
    
    for categories, generator in generators:
      for category in categories:
        self.registry[category] = generator
    
  def generate(self, category: str, value: str):
    generator = self.registry.get(category)
    if generator:
      generated_values = generator.generate(category=category, value=value)
      return generated_values
    else:
      raise ValueError(f"No generator found for category: {category}")