from datetime import datetime
import os
import pandas as pd
from evaluate import load

import rootutils
rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)

from core.model.inference.inference import Inference
from core.model.inference.hybrid_inference import HybirdInference
from core.model.inference.multi_model import MultiModelInference
from core.common.utils import save_data_to_file
from core.config.model_config import (
    SAVED_EVAL_DIR,
    SAVED_EVAL_FILE,
)
from core.config.regex_config import (
    CORRECT_SPELLING_DICT,
    INFERENCE_REGEX_RULES
)
 


class Eval():
  def __init__(self, file_path: str, model_name: str, metric_name: str, inference_mode: str):
    self.file_path = file_path
    self.model_name = model_name
    self.inference_mode = inference_mode
    self.get_metric(metric_name=metric_name)
    self.get_inference_mode(inference_mode=inference_mode)
    
  def get_metric(self, metric_name: str):
    if metric_name=="exact_match":
      self.metric = load("exact_match")
      self.regexes_to_ignore = [" không trăm", " từ"]
    if metric_name=="bleu":
      pass
      
  def get_inference_mode(self, inference_mode: str):
    if inference_mode == "llm_inference":
      self.inference = Inference(data_path=self.file_path, model_name=self.model_name, correct_spelling_dict=CORRECT_SPELLING_DICT)
    elif inference_mode == "hybrid_inference":
      self.inference = HybirdInference(data_path=self.file_path, model_name=self.model_name, rules=INFERENCE_REGEX_RULES, correct_spelling_dict=CORRECT_SPELLING_DICT)
    elif inference_mode == "multimodel_inference":
      print("Multimodel_inference running")
      self.inference = MultiModelInference(data_path=self.file_path, model_name=self.model_name)
    
  def evaluate(self):
    results = []
    test_data = pd.read_csv(self.file_path)
    MAX_ENTRIES = 1
    
    save_eval_dir = os.path.join(SAVED_EVAL_DIR, self.inference_mode)
    model_name_path = f"{self.model_name.split('/')[-2]}_{self.model_name.split('/')[-1]}"
    saved_eval_file = f"{datetime.now().strftime('%H:%M:%S')}_{model_name_path}_{MAX_ENTRIES}_{SAVED_EVAL_FILE}"
    
    for _,row in test_data.iterrows():
      input = row["input"]
      label = row["s_output"]
      tagged_sentence = row["tagged_sentence"]
      gpt_tagged_sentence = row["gpt_tagged_sentence"]
      final_tags = row["final_tags"]
      test_tag = row["test_tag"]
      
      for i in range(MAX_ENTRIES):
        predicted_label = self.inference.infer_one(input=input)
        result = self.metric.compute(predictions=[predicted_label], references=[label], ignore_case=True, ignore_punctuation=True, regexes_to_ignore = self.regexes_to_ignore)
        exact_match_score = int(result["exact_match"])
        
        if exact_match_score == 1:
          break
        
      results.append(
          {"input": input,
          "label": label,
          "predicted_label": predicted_label,
          "tagged_sentence": tagged_sentence,
          "gpt_tagged_sentence": gpt_tagged_sentence,
          "final_tags": final_tags,
          "test_tag": test_tag,
          "exact_match": exact_match_score
          }
        )
      
      if len(results) == 10:
        save_data_to_file(results, save_eval_dir, saved_eval_file)
        results.clear()
    if results:
       save_data_to_file(results, save_eval_dir, saved_eval_file)
  
  
    
if __name__=="__main__":
  file_path="/data/datnt3/text-normalization/data_storage/train_test/2025-05-25/test_data_main.csv"
  model_name="/data/datnt3/text-normalization/core/model/saved/lora/2025-06-07/vn-qwen2.5-3b-augmented-2025-06-07"
  # model_name = ["/data/datnt3/text-normalization/core/model/saved/lora/2025-05-26/vn-llama3.2-3b-finetuned-300k",
  #               "/data/datnt3/text-normalization/core/model/saved/lora/2025-06-06/vn-llama3.2-3b-finetuned-300k-16k-30step/vn-llama3.2-3b-finetuned-300k-16k-30step"]
  
  eval = Eval(file_path=file_path, model_name=model_name, metric_name="exact_match", inference_mode="llm_inference")
  eval.evaluate()

  