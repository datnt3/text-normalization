import os
import random
import rootutils
import pandas as pd
from loguru import logger
from datetime import datetime

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)
from core.common.utils import save_data_to_file
from core.config.config import (
    NSW_LIST,
    REGEX_RULE_LIST,
    TEST_DATA_FILE,
    TEST_RATIO,
    TRAIN_DATA_FILE,
    TRAIN_TEST_DATA_DIR,
)
from core.data.dataset.dataset import TextNormDataset

os.makedirs("logs", exist_ok=True)

# Add log file
logger.add("logs/train_test_split.log", level="INFO")


class DataModule:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.setup()

    def train_test_data_split(self):
        logger.info(f"🚀 Starting train-test split at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        tags = []
        tagged_sentences = {}
        test_data = []
        train_data = []
        used_in_test_datas = []
        used_in_train_datas = []

        #FIXME: tags bi sai, thieu cacs loai nhap nhang score, ratio..
        text_norm_dataset = self.text_norm_dataset.data
        # for row in text_norm_dataset["final_tags"]:
        #     if pd.isna(row):
        #       continue
        #     row_tag_values = row.split(";")
        #     for row_tag_value in row_tag_values:
        #         if not row_tag_value in tags:
        #             tags.append(row_tag_value)
        # for item in REGEX_RULE_LIST:
        #     if item["tag"] != "":
        #         tags.append(item["tag"])
        # tags = list(set(tags))
        
        tags = NSW_LIST

        for index, row in text_norm_dataset.iterrows():
            final_tags = row.get("final_tags")
            if pd.isna(final_tags):
                continue
            for tag in tags:
                if tag in final_tags:
                    if not tag in tagged_sentences.keys():
                        tagged_sentences[tag] = []
                    tagged_sentences[tag].append(
                        {
                            "input": row["input"],
                            "s_output": row["s_output"],
                            "tagged_sentence": row["tagged_sentence"],
                            "tags": row["tags"],
                            "gpt_tagged_sentence": row["gpt_tagged_sentence"],
                            "gpt_tags": row["gpt_tags"],
                            "final_tags": row["final_tags"],
                            "test_tag": tag
                        }
                    )

        sorted_tagged_sentences = sorted(
            tagged_sentences.items(), key=lambda item: len(item[1])
        )

        for tag, sentences in sorted_tagged_sentences:
            random.seed(42)
            random.shuffle(sentences)

            filtered_sentences = []
            for sample in sentences:
                if sample["input"] in used_in_test_datas:
                    continue
                if sample["input"] in used_in_train_datas:
                    continue
                filtered_sentences.append(sample)

            if len(filtered_sentences) < 30:
                number_test_samples = 0
                logger.info(f"{tag}: {len(filtered_sentences)}")
                continue
            if len(filtered_sentences) > 30 and len(filtered_sentences) < 300:
                number_test_samples = int(TEST_RATIO * len(filtered_sentences))
                logger.info(
                    f"{tag}: {len(filtered_sentences)} filtered_sentences, test samples: {number_test_samples}"
                )
            else:
                number_test_samples = 50
                logger.info(
                    f"{tag}: {len(filtered_sentences)} filtered_sentences, test samples: {number_test_samples}"
                )

            for i in range(len(filtered_sentences)):
                if i < number_test_samples:
                    test_data.append(filtered_sentences[i])
                    used_in_test_datas.append(filtered_sentences[i]["input"])
                else:
                    train_data.append(filtered_sentences[i])
                    used_in_train_datas.append(filtered_sentences[i]["input"])

        save_data_to_file(test_data, TRAIN_TEST_DATA_DIR, TEST_DATA_FILE)
        save_data_to_file(train_data, TRAIN_TEST_DATA_DIR, TRAIN_DATA_FILE)

    def setup(self):
        self.text_norm_dataset = TextNormDataset(self.data_path)


if __name__ == "__main__":
    data_module = DataModule("data_storage/processed/retagged_data_cleaned_v4.csv")
    data_module.train_test_data_split()
