import os
import pandas as pd
import rootutils
rootutils.setup_root(__file__,
                     indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
                     pythonpath=True)
from datasets import Dataset

from core.config.config import LABELED_DATA_DIR, TRAIN_DATA_DIR

class DataPreprocessing():
    def __init__(self, labeled_data_path: str):
        self.labeled_data_path = labeled_data_path
        
    def format_data(self):
        df = pd.read_csv(self.labeled_data_path)
        conversations = []
        for index, row in df.iterrows():
            input = row["input"]
            s_output = row["s_output"]
            conversation = [{"role": "system",
                             "content": "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Do the following task."},
                            {"role": "user",
                             "content": f"Convert all the numerical non-standard words into its corresponding phonetic spoken Vietnamese form. \nInput: {input}\nOutput:"},
                            {"role": "assistant",
                             "content": f"{s_output}"}
                            ]
            conversations.append(conversation)
        
        df["conversation"] = conversations
        dataset = Dataset.from_pandas(df=df)
        train_data_path = os.path.join(LABELED_DATA_DIR, TRAIN_DATA_DIR)
        os.makedirs(train_data_path, exist_ok=True)
        dataset.save_to_disk(dataset_path=train_data_path)
        
if __name__=="__main__":
    data_preprocessing = DataPreprocessing("/Users/datnt/Desktop/code/text-normalization/data_storage/processed/vn-text-norm-25k.csv")
    data_preprocessing.format_data()