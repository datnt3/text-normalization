from typing import Dict, List

import pandas as pd


class DataClean():
  @staticmethod
  def normalize_data(df: pd.DataFrame) -> pd.DataFrame:
      for col in df.columns:
        df[col] = df[col].str.lower()
      return df
  
  @staticmethod
  def expand_abbreviation(expanded_abbs: Dict, df: pd.DataFrame, col: str):
      for expanded_word, abbs in expanded_abbs.items():
        for abb in abbs:
          df[col] = df[col].str.replace(abb, expanded_word)
      return df
        
        
if __name__ == "__main__":
  abbs = {
    "việt nam đồng": ["vnd", "vnđ", "₫"],
    "đô la mỹ": ["usd", "$"],
    "ơ-rô": ["euro", "eur", "€"],
    "bảng anh": ["£"]
  }
  file = "/Users/datnt/Desktop/code/text-normalization/data_storage/processed/retagged_data_cleaned.csv"
  df = pd.read_csv(file)
  
  df = DataClean().normalize_data(df=df)
  df = DataClean().expand_abbreviation(expanded_abbs=abbs, df=df, col="s_output")
  
  df.to_csv("/Users/datnt/Desktop/code/text-normalization/data_storage/processed/retagged_data_cleaned.csv", index=False)

