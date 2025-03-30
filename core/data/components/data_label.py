from typing import List
from openai import OpenAI
from core.config.config import (
    LABELED_DATA_DIR, LABELED_DATA_FILE, LOGGING_DATA_FILE, OPENAI_API_KEY, OPENAI_MODEL, USER_PROMPT
)
import logging
import pandas as pd
import os

logging.basicConfig(level=logging.DEBUG,
                    filename=LOGGING_DATA_FILE,
                    filemode='a',
                    encoding="utf-8",
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S')
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

    def label_data(self, raw_datas: List) -> List:
        labeled_datas = []
        for raw_data in raw_datas:
            logger.info(f"Processing paragraph {raw_datas.index(raw_data)}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system",
                     "content": "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Do the following task."},
                    {"role": "user",
                     "content": f"{USER_PROMPT}\n**Input**: {raw_data}\n**Output**:"}
                ]
            )

            result = response.choices[0].message.content
            labeled_datas.append(result)
            self.save_data_to_file(result)
            logger.info(
                f"Finish processing paragraph {raw_datas.index(raw_data)}\n{result}\n")
            logger.info("================================")

        return labeled_datas

    def save_datas_to_file(self, labeled_datas: List) -> None:
        data_dict = {"labeled_datas": labeled_datas}

        df = pd.DataFrame(data_dict)
        if not os.path.exists(LABELED_DATA_DIR):
            os.makedirs(LABELED_DATA_DIR, exist_ok=True)

        df.to_csv(os.path.join(LABELED_DATA_DIR, LABELED_DATA_FILE),
                  mode="a", index=False)

    def save_data_to_file(self, labeled_data: str) -> None:
        if not os.path.exists(LABELED_DATA_DIR):
            os.makedirs(LABELED_DATA_DIR, exist_ok=True)

        labeled_data_dict = {"labeled_data": [labeled_data]}
        
        df = pd.DataFrame(labeled_data_dict)
        df.to_csv(os.path.join(LABELED_DATA_DIR, LABELED_DATA_FILE),
                  mode='a', encoding='utf-8', index=False, header=False)
        
    #!DONE:
    # Save each paragraph to csv file after responsing
    #!TODO:
    # Continue processing from the last paragraph of the last file with true index
    # - Save index to a log file 
    # - Load the last index from log file and continue processing
    # Processing multiple .csv files in a turn
