from datetime import datetime
import os
import re
import pandas as pd
from evaluate import load
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from regex import Regex
from underthesea import word_tokenize

import rootutils

rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)

from core.n2w_handler.nsw_tag.base_rule import Rule
from core.model.inference.inference import Inference
from core.model.inference.hybrid_inference import HybirdInference
from core.model.inference.multi_model import MultiModelInference
from core.common.utils import save_data_to_file
from core.config.config import REGEX_RULE_LIST
from core.config.model_config import (
    SAVED_EVAL_DIR,
    SAVED_EVAL_FILE,
)
from core.config.regex_config import CORRECT_SPELLING_DICT, INFERENCE_REGEX_RULES


class Eval:
    def __init__(
        self, file_path: str, model_name: str, metric_name: str, inference_mode: str
    ):
        self.file_path = file_path
        self.model_name = model_name
        self.inference_mode = inference_mode
        self.get_metric(metric_name=metric_name)
        self.get_inference_mode(inference_mode=inference_mode)
        self.rule = Rule(REGEX_RULE_LIST)

    def get_metric(self, metric_name: str):
        if metric_name == "exact_match":
            self.metric = load("exact_match")
            self.regexes_to_ignore = [" không trăm", " từ"]
        if metric_name == "bleu":
            pass

    def get_inference_mode(self, inference_mode: str):
        if inference_mode == "llm_inference":
            self.inference = Inference(
                data_path=self.file_path,
                model_name=self.model_name,
                correct_spelling_dict=CORRECT_SPELLING_DICT,
            )
        elif inference_mode == "hybrid_inference":
            self.inference = HybirdInference(
                data_path=self.file_path,
                model_name=self.model_name,
                rules=INFERENCE_REGEX_RULES,
                correct_spelling_dict=CORRECT_SPELLING_DICT,
            )
        elif inference_mode == "multimodel_inference":
            print("Multimodel_inference running")
            self.inference = MultiModelInference(
                data_path=self.file_path, model_name=self.model_name
            )
    def get_saved_location(self, max_entries: int):
        if "llama" in self.model_name or "qwen" in self.model_name:
            save_eval_dir = os.path.join(SAVED_EVAL_DIR, self.inference_mode)
            model_name_path = (
                f"{self.model_name.split('/')[-2]}_{self.model_name.split('/')[-1]}"
            )
            saved_eval_file = f"{datetime.now().strftime('%H:%M:%S')}_{model_name_path}_{max_entries}_{SAVED_EVAL_FILE}"
        if "vinorm" in self.model_name or "gpt" in self.model_name or "gemini" in self.model_name:
            save_eval_dir = os.path.join(SAVED_EVAL_DIR, self.inference_mode)
            saved_eval_file = f"{datetime.now().strftime('%H:%M:%S')}_{self.model_name}_{max_entries}_{SAVED_EVAL_FILE}"
            
        return save_eval_dir, saved_eval_file
        
    def remove_punc(self, prediction: str, label: str):
        prediction = re.sub(r"[^\w\s]", "", prediction)
        prediction = re.sub(r"\s+", " ", prediction).strip()
        label = re.sub(r"[^\w\s]", "", label)
        label = re.sub(r"\s+", " ", label).strip()
        return prediction, label
    
    def get_exact_match_score(self, prediction: str, label: str):
        result = self.metric.compute(
                    predictions=[prediction],
                    references=[label],
                    ignore_case=True,
                    ignore_punctuation=True,
                    regexes_to_ignore=self.regexes_to_ignore,
                )
        exact_match_score = int(result["exact_match"])
        
        return exact_match_score
    
    def get_bleu_score(self, prediction: str, label: str):
        prediction = word_tokenize(prediction, format="text")
        label = [word_tokenize(label, format="text")]
        smoothing_function = SmoothingFunction().method4
        
        bleu1 = sentence_bleu(label, prediction, weights=(1, 0, 0, 0), smoothing_function=smoothing_function)
        bleu2 = sentence_bleu(label, prediction, weights=(0.5, 0.5, 0, 0), smoothing_function=smoothing_function)
        bleu3 = sentence_bleu(label, prediction, weights=(0.33, 0.33, 0.33, 0), smoothing_function=smoothing_function)
        bleu4 = sentence_bleu(label, prediction, weights=(0.25, 0.25, 0.25, 0.25), smoothing_function=smoothing_function)
        
        return bleu1, bleu2, bleu3, bleu4
    
    def get_nsw_exact_match_score(self, tagged_sentence: str, exact_match_score: int):
        nsw_exact_match = {}
        matches = self.rule.get_all_matches(sentence=tagged_sentence)
        if exact_match_score == 1:
            for match in matches:
                nsw = match.group(1)
                tag = match.group(2)
                nsw_exact_match[nsw] = [tag, 1]
        else:
            for match in matches:
                nsw = match.group(1)
                tag = match.group(2)
                nsw_exact_match[nsw] = [tag, 0]
                
        return nsw_exact_match
    
    def evaluate(self):
        results = []
        test_data = pd.read_csv(self.file_path)
        MAX_ENTRIES = 1

        save_eval_dir, saved_eval_file = self.get_saved_location(max_entries=MAX_ENTRIES)

        for _, row in test_data.iterrows():
            input = row["input"]
            label = row["s_output"]
            tagged_sentence = row["tagged_sentence"]
            gpt_tagged_sentence = row["gpt_tagged_sentence"]
            final_tags = row["final_tags"]
            test_tag = row["test_tag"]

            for i in range(MAX_ENTRIES):
                predicted_label = self.inference.infer_one(input=input)
                predicted_label, label = self.remove_punc(
                    prediction=predicted_label, label=label
                )
                exact_match_score = self.get_exact_match_score( 
                    prediction=predicted_label, label=label
                )
                if exact_match_score == 1:
                    bleu1, bleu2, bleu3, bleu4 = 1, 1, 1, 1
                    break
                bleu1, bleu2, bleu3, bleu4 = self.get_bleu_score(
                    prediction=predicted_label, label=label
                )
            
            if pd.isna(gpt_tagged_sentence):
                nsw_exact_match = self.get_nsw_exact_match_score(
                    tagged_sentence=tagged_sentence, exact_match_score=exact_match_score
                )
            else:
                nsw_exact_match = self.get_nsw_exact_match_score(
                    tagged_sentence=gpt_tagged_sentence, exact_match_score=exact_match_score
                )

            results.append(
                {
                    "input": input,
                    "label": label,
                    "predicted_label": predicted_label,
                    "tagged_sentence": tagged_sentence,
                    "gpt_tagged_sentence": gpt_tagged_sentence,
                    "final_tags": final_tags,
                    "test_tag": test_tag,
                    "exact_match": exact_match_score,
                    "bleu1": f"{bleu1:.2f}",
                    "bleu2": f"{bleu2:.2f}",
                    "bleu3": f"{bleu3:.2f}",
                    "bleu4": f"{bleu4:.2f}",
                    "nsw_exact_match": nsw_exact_match
                }
            )

            if len(results) == 1:
                save_data_to_file(results, save_eval_dir, saved_eval_file)
                results.clear()
        if results:
            save_data_to_file(results, save_eval_dir, saved_eval_file)


if __name__ == "__main__":
    file_path = "data_storage/train_test/2025-05-25/test_data_main.csv"
    model_name = "gpt-4o-mini"
    eval = Eval(
        file_path=file_path,
        model_name=model_name,
        metric_name="exact_match",
        inference_mode="llm_inference",
    )
    eval.evaluate()
