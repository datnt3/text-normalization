from typing import List

import rootutils
rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)

from core.n2w_handler.nsw_tag.base_rule import Rule
from core.n2w_handler.nsw_normalizer import NSWNormalizer

class PreProcessor():
    """
    PreProcessor class for text normalization.
    This class is responsible for preprocessing the input text before it is passed to the model.
    """

    def __init__(self, rules: List):
      self.rule = Rule(rules=rules)
      self.nsw_normalizer = NSWNormalizer()
      pass
    
    def preprocess(self, raw_text: str) -> str:
      nsw_match_names = self.rule.apply_rule(raw_sentence=raw_text)
      nsw_tagged_text,_ = self.rule.tag_sentence(raw_sentence=raw_text, match_names=nsw_match_names)
      
      match_infos = []
      matches = self.rule.get_all_matches(sentence=nsw_tagged_text)
      for match in matches:
        match_infos.append((match.start(), match.end(), match.group(1), match.group(2)))
      match_infos.sort(reverse=True, key=lambda x: x[0])    

      processed_text = nsw_tagged_text
      for start, end, value, category in match_infos:
        value = value.strip()
        print(type(value))
        print(f"Match found: {match.group()} with value: {value} and category: {category}")
        spoken_word = self.nsw_normalizer.convert(category=category, value=value)
        processed_text = processed_text[:start] + spoken_word + processed_text[end:]

      return processed_text
    
if __name__ == "__main__":
    # Example usage
    rules = [
        {
        "name": "dmdmy",
        "pattern": r"(?<![\w\/\.])(?:(ngày|ngay)\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[-–—−]\s*(?:(ngày|ngay)\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 1,
        },
        {
        "name": "ddmy",
        "pattern": r"(?<![\w\/\.])(?:(ngày|ngay)\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[-–—−]\s*(?:(ngày|ngay)\s?)?(0?[1-9]|[12][0-9]|3[01])\s*[\.\/]\s*(0?[1-9]|1[0-2])\s*[\.\/]\s*([1-9][0-9]{2,3})(?![\w\/])",
        "priority": 2,
        },
    ]
    
    preprocessor = PreProcessor(rules=rules)
    raw_text = """theo một nghiên cứu nửa đầu năm 2021 của cbre, tín hiệu khả quan đến từ một số địa phương như thanh hóa khi 6 tháng đầu năm 2021, lượng khách du lịch tăng 41,2% so với cùng kỳ 2020, hay phú quốc trong 4 ngày nghỉ lễ (30/4 - 3/5/2021) lượng khách tăng 13,5% so với cùng thời điểm năm trước."""
    processed_text = preprocessor.preprocess(raw_text)
    print(processed_text)  # Output will depend on the NSWNormalizer implementation


