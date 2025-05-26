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
from core.config.config import (
    TRAIN_TEST_DATA_DIR,
    TEST_DATA_FILE
)

class Inference():
  def __init__(self, data_path: str, model_name: str):
    self.data_path = data_path
    self.model_name = model_name
    self.get_merged_model(model_name=self.model_name)
  
  def get_merged_model(self, model_name: str):
    self.model, self.tokenizer = FastLanguageModel.from_pretrained(
      model_name=os.path.join(SAVED_MODEL_DIR, model_name),
      max_seq_length=MAX_SEQ_LENGTH,
      dtype=DTYPE,
      load_in_4bit=LOAD_IN_4BIT
    )
    
  def infer_all(self):
    FastLanguageModel.for_inference(self.model)
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
    messages = [
    {"role": "system",
    "content": INFER_SYS_PROMPT},
    {"role": "user", 
    "content": f"""Convert the NSWs in the below sentence to spoken words: {input}"""}
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
    
    return predicted_label
  
if __name__ == "__main__":
  test_data_path = os.path.join(TRAIN_TEST_DATA_DIR, TEST_DATA_FILE)
  model_name = MODEL_NAME
  inference = Inference(data_path=test_data_path, model_name=model_name)

  inference.infer_all()
  
    