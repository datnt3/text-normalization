

from typing import Dict


class PostProcessor():
    def __init__(self, correct_spelling_dict: Dict):
        self.correct_spelling_dict = correct_spelling_dict
        pass
      
    def correct_spelling(self, text: str) -> str:
        for wrong_word, correct_word in self.correct_spelling_dict.items():
            text = text.replace(wrong_word, correct_word)
        text = text.replace("  ", " ").strip()
        return text

    def postprocess(self, text: str) -> str:
        corrected_text = self.correct_spelling(text)
        
        return corrected_text
