from datetime import datetime
import os
import pandas as pd
import rootutils
rootutils.setup_root(__file__,
                     indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
                     pythonpath=True)
from datasets import Dataset

from core.config.config import LABELED_DATA_DIR, TRAIN_DATA_DIR
from core.config.file_config import (
    AUGMENTED_DATASET,
    DATASET_DIR,
    ENHANCED_DATASET,
    GWEN_DATASET
)
from core.common.utils import save_dataset

class DataPreprocessing():
    def __init__(self, labeled_data_path: str):
        self.labeled_data_path = labeled_data_path
        
    def format_data(self, category: str):
        if category == "llama":
            df = pd.read_csv(self.labeled_data_path)
            conversations = []
            for index, row in df.iterrows():
                input = row["input"]
                output = row["output"]
                conversation = [{"role": "system",
                                "content": "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Do the following task."},
                                {"role": "user",
                                "content": f"Convert all the numerical non-standard words into its corresponding phonetic spoken Vietnamese form. \nInput: {input}\nOutput:"},
                                {"role": "assistant",
                                "content": f"{output}"}
                                ]
                conversations.append(conversation)
            
            df["conversation"] = conversations
            save_dataset(df=df, saved_dir=DATASET_DIR, dataset_name=AUGMENTED_DATASET)
        if category == "gwen":
            df = pd.read_csv(self.labeled_data_path)
            df["instruction"] = (
                "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Convert all the numerical non-standard words into its corresponding phonetic spoken Vietnamese form."
            )
            print(df.head(5))
            save_dataset(df=df, saved_dir=DATASET_DIR, dataset_name=GWEN_DATASET)

        
if __name__=="__main__":
    data_preprocessing = DataPreprocessing("/data/datnt3/text-normalization/data_storage/train_test/2025-06-07/augmented_train_data.csv")
    data_preprocessing.format_data(category="gwen")