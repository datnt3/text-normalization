import re
from typing import Dict, List
from unsloth import FastLanguageModel
from transformers import TextStreamer, TextIteratorStreamer
import pandas as pd
import os

import rootutils
rootutils.setup_root(
    __file__,
    indicator=(".project-root", "setup.cfg", "setup.py", ".git", "pyproject.toml"),
    pythonpath=True,
)
from core.common.utils import save_data_to_file
from core.model.inference.base import BaseInference
from core.model.inference.preprocessor import PreProcessor
from core.model.inference.postprocessor import PostProcessor
from core.config.model_config import (
    DTYPE,
    INFER_SYS_PROMPT,
    LOAD_IN_4BIT,
    MAX_SEQ_LENGTH,
    MODEL_NAME,
    SAVED_EVAL_DIR,
    SAVED_EVAL_FILE,
    SAVED_MODEL_DIR,
)
from core.config.regex_config import (
    CORRECT_SPELLING_DICT,
    INFERENCE_REGEX_RULES
)


class HybirdInference(BaseInference):
  def __init__(self, data_path: str, model_name: str, rules: List, correct_spelling_dict: Dict):
    self.data_path = data_path
    self.model_name = model_name
    self.get_merged_model(model_name=self.model_name)
    self.preprocessor = PreProcessor(rules=rules)
    self.postprocessor = PostProcessor(correct_spelling_dict=correct_spelling_dict)
  
  def get_merged_model(self, model_name: str):
    self.model, self.tokenizer = FastLanguageModel.from_pretrained(
      model_name=os.path.join(SAVED_MODEL_DIR, model_name),
      max_seq_length=MAX_SEQ_LENGTH,
      dtype=DTYPE,
      load_in_4bit=LOAD_IN_4BIT
    )
    
    FastLanguageModel.for_inference(self.model)
    
  
    
  def infer_all(self):
    results = []

    test_data = pd.read_csv(self.data_path)
    for _,row in test_data.iterrows():
      input = row["input"]
      label = row["s_output"]
      tagged_sentence = row["tagged_sentence"]
      gpt_tagged_sentence = row["gpt_tagged_sentence"]
      final_tags = row["final_tags"]
      try:
        predicted_label = self.infer_one(input=input)
      except Exception as e:
        print(f"Inference error: {e}")

      results.append(
        {"input": input,
        "label": label,
        "predicted_label": predicted_label,
        "tagged_sentence": tagged_sentence,
        "gpt_tagged_sentence": gpt_tagged_sentence,
        "final_tags": final_tags
        }
      )
      
      if len(results) == 10:
        save_data_to_file(results, SAVED_EVAL_DIR, SAVED_EVAL_FILE.format(model_name=self.model_name))
        results.clear()
    if results:
        save_data_to_file(results, SAVED_EVAL_DIR, SAVED_EVAL_FILE.format(model_name=self.model_name))
        
      
  def infer_one(self, input: str) -> str:
    processed_text = self.preprocessor.preprocess(raw_text=input)
    if not re.search(r"\d", processed_text):
      processed_text = self.postprocessor.postprocess(text=processed_text)
      return processed_text
    
    messages = [
    {"role": "system",
    "content": INFER_SYS_PROMPT},
    {"role": "user", 
    "content": f"""Convert the NSWs in the below sentence to spoken words: {processed_text}"""}
    ]
    inputs = self.tokenizer.apply_chat_template(
      messages,
      tokenize = True,
      add_generation_prompt = True,
      return_tensors = "pt"
    ).to("cuda")
    
    streamer = TextIteratorStreamer(self.tokenizer, skip_prompt = True, skip_special_tokens=True)
    
    generation_kwargs = {
      "input_ids": inputs,
      "streamer": streamer,
      "max_new_tokens": 512,
      "use_cache": True,
      "temperature": 1.5,
      "top_p": 0.9
    }
    
    self.model.generate(**generation_kwargs)
    predicted_label = "".join([token for token in streamer])
    predicted_label = predicted_label.strip()
    
    predicted_label = self.postprocessor.postprocess(text=predicted_label)
    
    return predicted_label
  
if __name__ == "__main__":
  input_sample = """bình quân mỗi ngày có khoảng 20.000 cuộc gọi của công dân đến tổng đài hỗ trợ giải đáp thắc mắc, tiếp nhận thông tin về cấp, trả căn cước công dân (cccd) gắn chip (tổng đài 19000368 - pv) để hỏi các vấn đề liên quan, ngày cao điểm số cuộc gọi có thể lên tới 30.000."""
  file = "/data/datnt3/text-normalization/data_storage/train_test/2025-05-25/eval_test_data.csv"
  model_name = "/data/datnt3/text-normalization/core/model/saved/lora/2025-05-26/vn-llama3.2-1b-finetuned-300k"
  
  hybrid_inference = HybirdInference(data_path=file, model_name=model_name, rules=INFERENCE_REGEX_RULES, correct_spelling_dict=CORRECT_SPELLING_DICT)
  print(hybrid_inference.infer_one(input=input_sample))