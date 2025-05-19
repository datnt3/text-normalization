from torch.utils.data import Dataset
import pandas as pd


class TextNormDataset(Dataset):
  def __init__(self, data_path: str):
    self.data_path = data_path
    self.setup()
    
  def load_data(self) -> pd.DataFrame:
    data = pd.read_csv(self.data_path)
    
    return data
  
  def __len__(self):
    return self.data.shape[0]
  
  def __getitem__(self, index):
    return self.data.iloc[index]
    
  def setup(self):
    data = self.load_data()
    self.data = data
  