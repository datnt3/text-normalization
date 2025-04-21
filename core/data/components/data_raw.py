import os
import pandas as pd
from typing import List

from core.common.utils import load_checkpoints

class DataRaw(object):
  @staticmethod
  def get_data(path: str, column: str="text") -> List[str]:
    data = pd.read_csv(path)
    data = data.dropna()
    
    return data[column].to_list()
  
  @staticmethod
  def get_paths(dir_path: str) -> List[str]:
    paths = []
    for dir, sub_dirs, files in os.walk(dir_path):
      for file in files:
        path = os.path.join(dir, file)
        paths.append(path)
    paths.sort()
    return paths
  
  @staticmethod
  def cut_datas(paths: List[str]):
    file, index = load_checkpoints()
    if file is None:
      indexes = [0] * len(paths)
      return paths, indexes
    else:
      indexes = [index] + [0] * (len(paths) - 1)
      return paths[paths.index(file):], indexes
  
  @staticmethod
  def get_generator_data(dir_path: str):
    paths = DataRaw.get_paths(dir_path)
    paths, indexes = DataRaw.cut_datas(paths=paths)
    
    for path, index in list(zip(paths, indexes)):
      yield path, DataRaw.get_data(path), index
