from typing import Dict, List, Union
from core.common.utils import check_sentence, save_checkpoints
from openai import OpenAI
from core.config.config import (
    LABELED_DATA_DIR,
    LABELED_DATA_FILE,
    LOGGING_CONFIG_FILE,
    OPENAI_API_KEY,
    OPENAI_MODEL, 
    USER_PROMPT_FINAL
)
import logging
import logging.config
import pandas as pd
import os
import json
import re

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
                {"role": "system",
                 "content": SYSTEM_PROMPT},
                {"role": "user",
                 "content": user_prompt}
            ]
        )
        meta_prompt = response.choices[0].message.content

        return meta_prompt

    def label_data(self, raw_datas_generator) -> None:
        for path, raw_datas, idx in raw_datas_generator:
            for raw_data in raw_datas[idx:]:
                save_checkpoints(file=path, index=raw_datas.index(raw_data))
                try:
                    logger.info(f"Processing paragraph {raw_datas.index(raw_data)}")
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=[
                            {"role": "system",
                            "content": "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Do the following task."},
                            {"role": "user",
                            "content": f"{USER_PROMPT_FINAL}\n**Input**: {raw_data}\n**Output**:"}
                        ]
                    )

                    result = response.choices[0].message.content
                    result = str(result).replace("```json", "").replace("```", "")
                    labeled_datas = json.loads(result)
                    filtered_datas = self.save_data_to_file(labeled_datas=labeled_datas)
                    logger.info(
                        f"Finish processing paragraph {raw_datas.index(raw_data)}\n{filtered_datas}\n")
                    logger.info("================================")
                except:
                    continue
        
    def save_data_to_file(self, labeled_datas: Union[List, Dict]) -> List:
        if isinstance(labeled_datas, Dict):
            labeled_datas = [labeled_datas]
        filtered_datas = []
        # Check labeled_datas, remove sentences which do not contain numerical NSWs
        for labeled_data in labeled_datas:
            if check_sentence(labeled_data["input"]):
                filtered_datas.append(labeled_data)
        
        if not os.path.exists(LABELED_DATA_DIR):
            os.makedirs(LABELED_DATA_DIR, exist_ok=True)

        df = pd.DataFrame(filtered_datas)
        saved_path = os.path.join(LABELED_DATA_DIR, LABELED_DATA_FILE)
        file_exist = os.path.isfile(saved_path)
        df.to_csv(saved_path, mode='a', encoding='utf-8', index=False, header=not file_exist)
        
        return filtered_datas

        #!DONE:
        # Save each paragraph to csv file after responsing
        #!TODO:
        # 1. Continue processing from the last paragraph of the last file with true index
        # - Save index to a json file
        # - Load the last index from log file and continue processing
        # 2. Refactor save_data_to_file: save both raw and formatted data into 2 columns
        # Processing multiple .csv files in a turn
