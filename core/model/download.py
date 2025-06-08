from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "unsloth/Qwen2.5-3B-Instruct"
saved_path = "./core/model/saved//base/Qwen2.5-3B-Instruct"


# Load model and tokenizer from Hugging Face Hub
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Save them locally
model.save_pretrained(saved_path)
tokenizer.save_pretrained(saved_path)

print(f"✅ Model and tokenizer saved to {saved_path}")
