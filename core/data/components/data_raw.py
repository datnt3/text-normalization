import pandas as pd
from typing import List

class DataRaw(object):
  @staticmethod
  def get_data(path: str, column: str="text") -> List[str]:
    data = pd.read_csv(path)
    data = data.dropna()
    
    return data[column].to_list()
