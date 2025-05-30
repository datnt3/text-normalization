import pandas as pd
import re

import rootutils

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)

from core.n2w_handler.nsw_tag.base_rule import Rule
from core.n2w_handler.nsw_normalizer import NSWNormalizer
from core.config.regex_config import INFERENCE_REGEX_RULES
from core.common.utils import (
    save_data_to_file,
    contains_arabic_number,
    contains_roman_number
)


class DataEnhancement():
  def __init__(self, file_path: str, rules: list):
    self.file_path = file_path
    self.rule = Rule(rules=rules)
    self.nsw_normalizer = NSWNormalizer() 
    
  def pad_sentence(self, sentence: str, start: int, end: int):
    left_part = sentence[:start]
    right_part = sentence[end:]
    
    
    left_part = left_part.strip()
    if left_part:
      res_left_part = left_part
      left_part_words = left_part.split(" ") 
      for i in range(len(left_part_words)-1, -1, -1):
        if contains_arabic_number(left_part_words[i]) or contains_roman_number(left_part_words[i]):
          res_left_part = " ".join(left_part_words[i+1:])
          break
    else:
      res_left_part = ""

    right_part = right_part.strip()
    if right_part:
      res_right_part = right_part
      right_part_words = right_part.split(" ")
      for i in range(len(right_part_words)):
        if contains_arabic_number(right_part_words[i]) or contains_roman_number(right_part_words[i]):
          res_right_part = " ".join(right_part_words[:i])
          break
    else:
      res_right_part = ""
        
    return res_left_part, res_right_part
  
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
  
  def enhance_data(self):
    raw_train_data = pd.read_csv(self.file_path, encoding='utf-8')
    
    enhanced_train_data = []
    enhanced_part_train_data = {}

    for _, row in raw_train_data.iterrows():
        raw_sentence = row["input"]

        match_infos, nsw_tagged_text = self.get_match_infos(raw_sentence)
        
        for match_start, match_end, match_nsw, match_category in match_infos:
          left_part, right_part = self.pad_sentence(nsw_tagged_text, match_start, match_end)
          if left_part != "":
            left_part += " "
          if right_part != "":
            right_part = " " + right_part
          
          padding_inp = left_part + match_nsw + right_part
          
          spoken_word = self.nsw_normalizer.convert(category=match_category, value=match_nsw)
          padding_output = left_part + spoken_word + right_part
          
          enhanced_data = {
            "input": padding_inp.strip(),
            "output": padding_output.strip(),
            "raw_sentence": raw_sentence,
            "nsw": match_nsw,
            "tag": match_category,
          }
          
          enhanced_train_data.append(enhanced_data)
          if match_category not in enhanced_part_train_data.keys():
            enhanced_part_train_data[match_category] = []
          enhanced_part_train_data[match_category].append(enhanced_data)
          
          if len(enhanced_train_data) == 10:
            enhanced_train_data_csv = save_data_to_file(enhanced_train_data, saved_dir="data_storage/train_test/enhanced", saved_file="enhanced_train_data.csv")
            enhanced_train_data.clear()

          for category, enhanced_data_list in enhanced_part_train_data.items():
            if len(enhanced_data_list) == 10:
              enhanced_part_train_data_csv = save_data_to_file(enhanced_data_list, saved_dir="data_storage/train_test/enhanced", saved_file=f"{category}_enhanced_part_train_data.csv")
              enhanced_part_train_data[category].clear()

    if enhanced_train_data:
        enhanced_train_data_csv = save_data_to_file(enhanced_train_data, saved_dir="data_storage/train_test/enhanced", saved_file="enhanced_train_data.csv")
        
    for category, enhanced_data_list in enhanced_part_train_data.items():
            if enhanced_data_list:
              enhanced_part_train_data_csv = save_data_to_file(enhanced_data_list, saved_dir="data_storage/train_test/enhanced", saved_file=f"{category}_enhanced_part_train_data.csv")
              
if __name__ == "__main__":
  train_file_path = "/data/datnt3/text-normalization/data_storage/train_test/2025-05-25/train_data.csv"
  rules = INFERENCE_REGEX_RULES
  data_enhancement = DataEnhancement(file_path=train_file_path, rules=rules)
  
  data_enhancement.enhance_data()
    
    