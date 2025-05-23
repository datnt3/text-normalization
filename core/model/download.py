from transformers import AutoTokenizer, AutoModelForCausalLM

# Load model and tokenizer from Hugging Face Hub
model = AutoModelForCausalLM.from_pretrained("unsloth/Llama-3.2-1B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("unsloth/Llama-3.2-1B-Instruct")

# Save them locally
model.save_pretrained("./core/model/base/llama-3.2-1b-instruct")
tokenizer.save_pretrained("./core/model/base/llama-3.2-1b-instruct")

print("✅ Model and tokenizer saved to ./llama-3.2-1b-instruct")
