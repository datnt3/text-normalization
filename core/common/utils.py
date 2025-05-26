from datetime import datetime
import re
import os
import json
from typing import Dict, List, Union
import pandas as pd

from core.config.config import CONFUSED_NSW_DICT, NSW_TAG_PROMPT

def check_sentence(sentence: str) -> bool:
    if re.search(r'\d', sentence) is None:
        return False
    else:
        return True

def save_checkpoints(file: str, index: int, saved_dir: str, saved_file: str) -> None:
    checkpoint = {"file": file, "index": index}

    if not os.path.exists(saved_dir):
        os.makedirs(saved_dir, exist_ok=True)

    with open(os.path.join(saved_dir, saved_file), mode='w', encoding='utf-8') as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=4)

def load_checkpoints(saved_dir: str, saved_file: str):
    checkpoint_path = os.path.join(saved_dir, saved_file)
    if os.path.isfile(checkpoint_path):
        with open(checkpoint_path) as f:
            checkpoint = json.load(f)
            file = checkpoint["file"]
            index = checkpoint["index"]
            return file, index
    return None, 0

def save_data_to_file(labeled_datas: Union[List, Dict], saved_dir: str, saved_file: str) -> List:
    if isinstance(labeled_datas, Dict):
        labeled_datas = [labeled_datas]
    filtered_datas = []
    # Check labeled_datas, remove sentences which do not contain numerical NSWs
    for labeled_data in labeled_datas:
        if check_sentence(labeled_data["input"]):
            filtered_datas.append(labeled_data)
    
    os.makedirs(os.path.join(saved_dir, datetime.now().strftime("%Y-%m-%d")), exist_ok=True)

    df = pd.DataFrame(filtered_datas)
    saved_path = os.path.join(saved_dir, datetime.now().strftime("%Y-%m-%d"), saved_file)
    file_exist = os.path.isfile(saved_path)
    df.to_csv(saved_path, mode='a', encoding='utf-8', index=False, header=not file_exist)
    
    return filtered_datas

def format_prompt(input: str, category: str):
    formatted_prompt = NSW_TAG_PROMPT.format(
        category = category,
        true_labels = CONFUSED_NSW_DICT[category]["true_labels"],
        examples = CONFUSED_NSW_DICT[category]["examples"]
    )
    prompt = f"{formatted_prompt}\nInput:\n{input}\nOutput:"

    return prompt

