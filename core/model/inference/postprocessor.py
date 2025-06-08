from typing import Dict

import rootutils
rootutils.setup_root(__file__,
                     indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
                     pythonpath=True)
from datasets import Dataset

from core.config.regex_config import CORRECT_SPELLING_DICT


class PostProcessor():
    def __init__(self, correct_spelling_dict: Dict):
        self.correct_spelling_dict = correct_spelling_dict
        pass
      
    def correct_spelling(self, text: str) -> str:
        for correct_word, wrong_words in self.correct_spelling_dict.items():
            for wrong_word in wrong_words:
                text = text.replace(wrong_word, correct_word)
        text = text.replace("  ", " ").strip()
        return text

    def postprocess(self, text: str) -> str:
        corrected_text = self.correct_spelling(text)
        
        return corrected_text
    
if __name__ == "__main__":
    postprocessor = PostProcessor(correct_spelling_dict=CORRECT_SPELLING_DICT)
    input_text = """hồ chủ tịch nói chuyện thân mật với cán bộ, nhân dân các dân tộc tỉnh lào cai trong dịp bác lên thăm tỉnh lào cai ngày hai mươi ba đến ngày hai mươi tư tháng chín năm một nghìn chín trăm năm mươi tám."""
    corrected_text = postprocessor.postprocess(input_text)
    
    print(corrected_text)  # Output: This is the best way to receive information, definitely!
