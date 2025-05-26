import pandas as pd
from evaluate import load


class Eval():
  def __init__(self, file: str):
    self.file = file
    pass
  
  def evaluate(self):
    file = pd.read_csv(self.file)
    exact_match_metric = load("exact_match")
    results = []
    regexes_to_ignore = [" mồng", " mùng", " không trăm", " ngàn", " nghìn"]
    for _, row in file.iterrows():
      
      result = exact_match_metric.compute(predictions=[row["predicted_label"]], references=[row["label"]], ignore_case=True, ignore_punctuation=True, regexes_to_ignore = regexes_to_ignore)
      result = int(result["exact_match"])
      results.append(result)
      
    file["exact_match_res"] = results
    file.to_csv("/data/datnt3/text-normalization/data_storage/eval/exact_match.csv", index=False, encoding="utf-8", mode="w")
    
if __name__=="__main__":
  eval = Eval("/data/datnt3/text-normalization/data_storage/eval/new_eval_vn-llama3.2-1b-finetuned-300k.csv")
  eval.evaluate()

  