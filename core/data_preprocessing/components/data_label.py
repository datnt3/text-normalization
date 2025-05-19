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

from core.data_preprocessing.components.nsw_tag.base_rule import Rule

logging.config.fileConfig(LOGGING_CONFIG_FILE)
logger = logging.getLogger()


class DataLabel(object):
    def __init__(self, api_key: str = OPENAI_API_KEY, model: str = OPENAI_MODEL):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_prompt(self, user_prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
        )
        meta_prompt = response.choices[0].message.content

        return meta_prompt

    def label_data(self, raw_datas_generator) -> None:
        for path, raw_datas, idx in raw_datas_generator:
            for raw_data in raw_datas[idx:]:
                save_checkpoints(
                    path,
                    raw_datas.index(raw_data),
                    DATA_CHECKPOINT_DIR,
                    DATA_CHECKPOINT_FILE,
                )
                try:
                    logger.info(f"Processing paragraph {raw_datas.index(raw_data)}")
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Do the following task.",
                            },
                            {
                                "role": "user",
                                "content": f"{USER_PROMPT_FINAL}\n**Input**: {raw_data}\n**Output**:",
                            },
                        ],
                    )

                    result = response.choices[0].message.content
                    result = str(result).replace("```json", "").replace("```", "")
                    labeled_datas = json.loads(result)
                    filtered_datas = save_data_to_file(
                        labeled_datas=labeled_datas,
                        saved_dir=LABELED_DATA_DIR,
                        saved_file=LABELED_DATA_FILE,
                    )
                    logger.info(
                        f"Finish processing paragraph {raw_datas.index(raw_data)}\n{filtered_datas}\n"
                    )
                    logger.info("================================")
                except:
                    continue

    def tag_data_nsw(self, file_path: str):
        file, index = load_checkpoints(DATA_CHECKPOINT_DIR, NSW_TAGGED_CHECKPOINT_FILE)
        if file is None:
            file = file_path
            index = 0
        gpt_label_data = pd.read_csv(file)
        inputs = gpt_label_data["input"].to_list()
        processed_data = gpt_label_data.iloc[index:]
        rule = Rule(REGEX_RULE_LIST)

        datas = []
        for index, row in processed_data.iterrows():
            try:
                is_confused = False
                input = row["input"]
                s_output = row["s_output"]
                match_names = rule.apply_rule(input)
                tagged_sentence, tags = rule.tag_sentence(input, match_names)
                # FIXME: Use GPT to classify sentence having NUM:NUM, NUM-NUM, NUM/NUM, NUM.NUM
                for tag in tags:
                    if tag in CONFUSED_NSW_DICT.keys():
                        is_confused = True
                        break
                
                if is_confused:
                    gpt_tagged_sentence, gpt_tags, original_tags = self.gpt_nsw_tag(
                        tags, CONFUSED_NSW_DICT.keys(), tagged_sentence
                    )
                    data = {
                        "input": input,
                        "s_ouput": s_output,
                        "tagged_sentence": tagged_sentence,
                        "tags": "; ".join(original_tags),
                        "gpt_tagged_sentence": gpt_tagged_sentence,
                        "gpt_tags": "; ".join(gpt_tags),
                    }
                else:
                    data = {
                        "input": input,
                        "s_ouput": s_output,
                        "tagged_sentence": tagged_sentence,
                        "tags": "; ".join(tags),
                        "gpt_tagged_sentence": "",
                        "gpt_tags": "",
                    }
            except:
                continue

            datas.append(data)

            if len(datas) == 10:
                # Get the real index of the data in the original gpt label file
                saved_index = inputs.index(datas[9]["input"])
                save_checkpoints(
                    file, saved_index, DATA_CHECKPOINT_DIR, NSW_TAGGED_CHECKPOINT_FILE
                )
                filtered_datas = save_data_to_file(
                    datas, saved_dir=LABELED_DATA_DIR, saved_file=NSW_TAGGED_DATA_FILE
                )
                datas.clear()

    def get_gpt_response(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Do the following task.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        result = response.choices[0].message.content
        result = str(result).replace("```json", "").replace("```", "")
        json_result = json.loads(result)

        return json_result

    def gpt_nsw_tag(self, tags: List, categories: List, input: str):
        gpt_tags = []
        original_tags = tags.copy()
        
        for category in categories:
            if category in tags:
                tags.remove(category)
                prompt = format_prompt(input=input, category=category)
                result = self.get_gpt_response(prompt=prompt)
                input = result["tagged_sentence"]
                result_tags = result["tags"].split(",")
                for result_tag in result_tags:
                    if result_tag not in gpt_tags:
                        gpt_tags.append(result_tag.strip())

        tagged_sentence = result["tagged_sentence"]
        tags.extend(gpt_tags)
        final_tags = list(set(tags))

        return tagged_sentence, final_tags, original_tags


if __name__ == "__main__":
    data_label = DataLabel()
    data_label.tag_data_nsw("data_storage/processed/processed_data.csv")
