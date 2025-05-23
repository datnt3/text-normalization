SAVED_MODEL_DIR = "/data/datnt3/text-normalization/core/model/saved/lora"
MODEL_NAME = "vn-llama3.2-1b-finetuned-300k"
MAX_SEQ_LENGTH = 2048 # Choose any! We auto support RoPE Scaling internally!
DTYPE = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
LOAD_IN_4BIT = False # Use 4bit quantization to reduce memory usage. Can be False.
INFER_SYS_PROMPT = "You are a phonetic Vietnamese specialist mastering in Text normalization task in Text To Speech. Convert each numerical non-standard word into its spoken phonetic Vietnamese form, integrating it back into the sentence."

SAVED_EVAL_DIR = "data_storage/eval"
SAVED_EVAL_FILE = "eval_{model_name}.csv"