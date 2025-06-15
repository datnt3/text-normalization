from typing import Dict, List, Union
import rootutils

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)
from core.common.utils import (
    check_sentence,
    format_prompt,
    load_checkpoints,
    save_checkpoints,
    save_data_to_file,
)
from openai import OpenAI
from core.config.config import (
    CONFUSED_NSW_DICT,
    DATA_CHECKPOINT_DIR,
    DATA_CHECKPOINT_FILE,
    LABELED_DATA_DIR,
    LABELED_DATA_FILE,
    LOGGING_CONFIG_FILE,
    NSW_TAGGED_CHECKPOINT_FILE,
    NSW_TAGGED_DATA_FILE,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    USER_PROMPT_FINAL,
    REGEX_RULE_LIST,
)
import logging
import logging.config
import pandas as pd
import os
import json
import re

from core.n2w_handler.nsw_tag.base_rule import Rule


if __name__ == "__main__":
    file = "/data/datnt3/text-normalization/data_storage/train_test/2025-06-07/augmented_train_data.csv"
    df = pd.read_csv(file, encoding="utf-8")
    rule = Rule(REGEX_RULE_LIST)
    datas = []
    
    for _, row in df.iterrows():
        input = row["input"]
        output = row["output"]
        tagged_sentence = row["tagged_sentence"]
        tags = row["tags"]
        if pd.isna(tagged_sentence):
            match_names = rule.apply_rule(input)
            tagged_sentence, _ = rule.tag_sentence(input, match_names)
            tagged_sentence = tagged_sentence.strip().lower()
            data = {
                "input": input,
                "output": output,
                "tagged_sentence": tagged_sentence,
                "tags": tags,
            }
        else:
            data = {
                "input": input,
                "output": output,
                "tagged_sentence": tagged_sentence,
                "tags": tags,
            }
        datas.append(data)
    save_data_to_file(datas, "data_storage/train_test", "add_tagged_sentence_train_data.csv")
            
