import re
from typing import List
import pandas as pd


class DataPreprocessing(object):
    """
    1. Regex to identify num/num, num-num, num.num -> Mark ~ #
    2. Padding 30 words each side from the ~#
    """

    def __init__(self, text_datas: List[str], config):
        self.text_datas = text_datas
        self.config = config

    def identify_nsw(self):
        processed_text_datas = []
        for text_data in self.text_datas:
            modified_text_data = text_data
            nsws = re.finditer(self.config.regex, text_data)
            nsws_list = []
            for nsw in nsws:
                nsw = nsw.group()
                nsws_list.append(nsw)

            nsws_list = list(set(nsws_list))
            for nsw in nsws_list:
                modified_text_data = modified_text_data.replace(nsw, f"~{nsw}#")
            processed_text_datas.append(modified_text_data)
        return processed_text_datas
    
    def extract_nsw_sentence(self, processed_text_datas: List[str]):
        nsw_sentences = []
        for processed_text_data in processed_text_datas:
            words = processed_text_data.split()
            for word in words:
                if "~" in word and "#" in word:
                    index = words.index(word)
                    sen_start_index = max(0, index-30)
                    sen_end_index = min(len(words)-1,index+30)
                    nsw_sentence = " ".join(words[sen_start_index:sen_end_index+1])
                    nsw_sentences.append(nsw_sentence)
        return nsw_sentences

        
