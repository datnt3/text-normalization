from typing import List
import pandas as pd
import rootutils

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)

from core.n2w_handler.nsw_tag.base_rule import Rule
from core.n2w_handler.nsw_normalizer import NSWNormalizer
from core.data_preprocessing.data_augmentation.number_generator.generator import Generator
from core.config.regex_config import AUGMENT_REGEX_RULES
from core.common.utils import (
    save_data_to_file,
    contains_arabic_number,
    contains_roman_number
)


class DataAugment:
    def __init__(self, file_path: str, rules: list):
        self.file_path = file_path
        self.rule = Rule(rules=rules)
        self.Generator = Generator()
        self.nsw_normalizer = NSWNormalizer()
        pass
    
    def get_match_infos(self, raw_sentence: str):
        match_infos = []
        
        nsw_match_names = self.rule.apply_rule(raw_sentence=raw_sentence)
        nsw_tagged_text,_ = self.rule.tag_sentence(raw_sentence=raw_sentence, match_names=nsw_match_names)
        
        matches = self.rule.get_all_matches(sentence=nsw_tagged_text)
        for match in matches:
            match_infos.append((match.start(), match.end(), match.group(1), match.group(2)))
            print(match.group())
            print(f"Match found: {match.group(1)} ({match.group(2)}) at positions {match.start()}-{match.end()}")
        match_infos.sort(reverse=True, key=lambda x: x[0])
        
        return match_infos, nsw_tagged_text
    
    def get_generated_labels(self, generated_list: List[str], category: str):
        augmented_nsw_labels = []
        for nsw in generated_list:
            nsw = nsw.strip()
            spoken_word = self.nsw_normalizer.convert(category=category, value=nsw)
            augmented_nsw_labels.append((nsw, spoken_word))
        return augmented_nsw_labels

    def data_augment(self):
        raw_train_data = pd.read_csv(self.file_path, encoding='utf-8')
    
        augmented_train_data = []
        for _, row in raw_train_data.iterrows():
            augmented_train_data.append(
                {
                    "input": row["input"],
                    "output": row["output"],
                    "raw_sentence": row["raw_sentence"],
                    "tag": row["tag"]
                }
            )
            raw_sentence = row["input"]

            match_infos, nsw_tagged_text = self.get_match_infos(raw_sentence)
            for match_start, match_end, match_nsw, match_category in match_infos:
                if match_start == 0:
                    left_part = ""
                else:
                    left_part = nsw_tagged_text[:match_start]
                if match_end == len(nsw_tagged_text):
                    right_part = ""
                else:
                    right_part = nsw_tagged_text[match_end:] 
                augmented_nsws = self.Generator.generate(category=match_category, value=match_nsw)
                augmented_nsw_labels = self.get_generated_labels(generated_list=augmented_nsws, category=match_category)
                
                for augmented_nsw, spoken_word in augmented_nsw_labels:
                    data = {
                        "input": left_part + augmented_nsw + right_part,
                        "output": left_part + spoken_word + right_part,
                        "raw_sentence": row["raw_sentence"],
                        "tag": match_category
                    }
                    augmented_train_data.append(data)
            augmented_train_data_csv = save_data_to_file(augmented_train_data, saved_dir="data_storage/train_test/augment", saved_file="augmented_train_data.csv")
            augmented_train_data.clear()
            
            
if __name__ == "__main__":
    file_path = "/data/datnt3/text-normalization/data_storage/train_test/enhanced/2025-05-30/enhanced_train_data.csv"
    rules = AUGMENT_REGEX_RULES 
    data_augment = DataAugment(file_path=file_path, rules=rules)
    data_augment.data_augment()
                    
                     