import re
import os
import json

from core.config.config import DATA_CHECKPOINT_DIR, DATA_CHECKPOINT_FILE

def check_sentence(sentence: str) -> bool:
    if re.search(r'\d', sentence) is None:
        return False
    else:
        return True

def save_checkpoints(file: str, index: int) -> None:
    checkpoint = {"file": file, "index": index}

    if not os.path.exists(DATA_CHECKPOINT_DIR):
        os.makedirs(DATA_CHECKPOINT_DIR, exist_ok=True)

    with open(os.path.join(DATA_CHECKPOINT_DIR, DATA_CHECKPOINT_FILE), mode='w', encoding='utf-8') as f:
        json.dump(checkpoint, f, ensure_ascii=False, indent=4)

def load_checkpoints():
    checkpoint_path = os.path.join(DATA_CHECKPOINT_DIR, DATA_CHECKPOINT_FILE)
    if os.path.isfile(checkpoint_path):
        with open(checkpoint_path) as f:
            checkpoint = json.load(f)
            file = checkpoint["file"]
            index = checkpoint["index"]
            return file, index
    return None, 0