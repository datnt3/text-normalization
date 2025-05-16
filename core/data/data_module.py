import random
import rootutils
import pandas as pd

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)
from core.common.utils import save_data_to_file
from core.config.config import TEST_DATA_FILE, TRAIN_DATA_FILE, TRAIN_TEST_DATA_DIR
from core.data.dataset.dataset import TextNormDataset


class DataModule:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.setup()

    def train_test_data_split(self):
        tags = []
        tagged_sentences = {}
        test_data = []
        train_data = []

        text_norm_dataset = self.text_norm_dataset.data
        for row in text_norm_dataset["gpt_tags"]:
            if pd.isna(row):
              continue
            row_tag_values = row.split(";")
            for row_tag_value in row_tag_values:
                if not row_tag_value in tags:
                    tags.append(row_tag_value)

        for index, row in text_norm_dataset.iterrows():
            gpt_tags = row.get("gpt_tags")
            if pd.isna(gpt_tags):
              continue
            for tag in tags:
                if tag in gpt_tags:
                    if not tag in tagged_sentences.keys():
                        tagged_sentences[tag] = []
                    tagged_sentences[tag].append(
                        {
                            "input": row["input"],
                            "s_output": row["s_ouput"],
                            "tagged_sentence": row["tagged_sentence"],
                            "tags": row["tags"],
                            "gpt_tagged_sentence": row["gpt_tagged_sentence"],
                            "gpt_tags": row["gpt_tags"],
                        }
                    )

        for tag, sentences in tagged_sentences.items():
            random.seed(42)
            random.shuffle(sentences)
            test_samples = sentences[:5]
            train_samples = sentences[5:]
            save_data_to_file(test_samples, TRAIN_TEST_DATA_DIR, TEST_DATA_FILE)
            save_data_to_file(train_samples, TRAIN_TEST_DATA_DIR, TRAIN_DATA_FILE)

    def setup(self):
        self.text_norm_dataset = TextNormDataset(self.data_path)


if __name__ == "__main__":
    data_module = DataModule("data_storage/processed/test_spilt.csv")
    data_module.train_test_data_split()
