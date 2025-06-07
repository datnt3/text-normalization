import random

class NumberRand():
  @staticmethod
  def day_rand(constraint: int = 0):
    if constraint == 0:
      return random.randint(1, 27)
    else:
      return random.randint(constraint + 1, 28)
  
  @staticmethod
  def month_rand(constraint: int = 0):
    if constraint == 0:
      return random.randint(1, 11)
    else:
      return random.randint(constraint + 1, 12)
  
  @staticmethod
  def year_rand(constraint: int = 0):
    if constraint == 0:
      return random.randint(1700, 2049)
    else:
      return random.randint(constraint + 1, 2050)
  
  @staticmethod
  def hour_rand(constraint: int = 0):
    if constraint == 0:
      return random.randint(0, 22)
    else:
      return random.randint(constraint + 1, 23)
    
  @staticmethod
  def tel_rand():
    return random.randint(1000, 9999)
  
  @staticmethod
  def minute_rand(constraint: int = 0):
    if constraint == 0:
      return random.randint(0, 58)
    else:
      return random.randint(constraint + 1, 59)
  
  @staticmethod
  def date_seperator_rand():
    return random.choice(["/", "."])
  
  @staticmethod
  def hour_min_postfix_rand():
    choice_value = random.randint(0, 1)
    if choice_value == 0:
      hour_postfix = random.choice(["h", "g"])
      min_postfix = random.choice(["p", "", "'", "\u2032"])
    else:
      hour_postfix = ":"
      min_postfix = ""
    return hour_postfix, min_postfix
