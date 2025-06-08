from typing import Dict
import unsloth
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
from core.config.config import TRAIN_TEST_DATA_DIR, TEST_DATA_FILE


class Inference(BaseInference):
    def __init__(self, data_path: str, model_name: str, correct_spelling_dict: Dict):
        self.data_path = data_path
        self.model_name = model_name
        self.get_merged_model(model_name=self.model_name)
        self.postprocessor = PostProcessor(correct_spelling_dict=correct_spelling_dict)

    def get_merged_model(self, model_name: str):
        self.model, self.tokenizer = FastLanguageModel.from_pretrained(
            model_name=os.path.join(SAVED_MODEL_DIR, model_name),
            max_seq_length=MAX_SEQ_LENGTH,
            dtype=DTYPE,
            load_in_4bit=LOAD_IN_4BIT,
        )

        FastLanguageModel.for_inference(self.model)

    def get_predicted_label(self, inputs) -> str:
        streamer = TextIteratorStreamer(
            self.tokenizer, skip_prompt=True, skip_special_tokens=True
        )

        generation_kwargs = {
            **inputs,
            "streamer": streamer,
            "max_new_tokens": 512,
            "use_cache": True,
            "temperature": 1.5,
            "top_p": 0.9,
        }

        self.model.generate(**generation_kwargs)
        predicted_label = "".join([token for token in streamer])
        predicted_label = predicted_label.strip()
        predicted_label = self.postprocessor.postprocess(text=predicted_label)
        print(f"Predicted label: {predicted_label}")

        return predicted_label

    def infer_all(self):
        results = []

        test_data = pd.read_csv(self.data_path)
        for _, row in test_data.iterrows():
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
                {
                    "input": input,
                    "label": label,
                    "predicted_label": predicted_label,
                    "tagged_sentence": tagged_sentence,
                    "gpt_tagged_sentence": gpt_tagged_sentence,
                    "final_tags": final_tags,
                }
            )

            if len(results) == 10:
                save_data_to_file(
                    results,
                    SAVED_EVAL_DIR,
                    SAVED_EVAL_FILE.format(model_name=self.model_name),
                )
                results.clear()
        if results:
            save_data_to_file(
                results,
                SAVED_EVAL_DIR,
                SAVED_EVAL_FILE.format(model_name=self.model_name),
            )

    def infer_one(self, input: str) -> str:
        if "llama" in self.model_name:
            messages = [
                {
                    "role": "system",
                    "content": INFER_SYS_PROMPT
                    + "Convert the NSWs in the below sentence to spoken words:",
                },
                {
                    "role": "user",
                    # "content": f"""Convert the NSWs in the below sentence to spoken words: {input}"""}
                    "content": f"""{input}""",
                },
            ]
            inputs = self.tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
            )
            inputs = {"input_ids": inputs.to("cuda")}

            predicted_label = self.get_predicted_label(inputs=inputs)

        if "qwen" in self.model_name:
            messages = f"""
            ### Instruction
            You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Convert all the numerical non-standard words into its corresponding phonetic spoken Vietnamese form.

            ### Input:
            {input}

            ### Response:
            
            """

            inputs = self.tokenizer([messages], return_tensors="pt").to("cuda")

            streamer = TextIteratorStreamer(
                self.tokenizer, skip_prompt=True, skip_special_tokens=True
            )

            generation_kwargs = {
                **inputs,
                "streamer": streamer,
                "max_new_tokens": 512,
                # "use_cache": True,
                # "temperature": 1.5,
                # "top_p": 0.9,
            }

            self.model.generate(**generation_kwargs)
            predicted_label = "".join([token for token in streamer])
            predicted_label = predicted_label.strip()
            predicted_label = self.postprocessor.postprocess(text=predicted_label)
            print(f"Predicted label: {predicted_label}")

            # inputs = {k: v.to("cuda") for k, v in inputs.items()}

            # predicted_label = self.get_predicted_label(inputs=inputs)

        return predicted_label
