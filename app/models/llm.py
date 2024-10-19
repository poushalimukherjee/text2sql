import os
from transformers import file_utils 
# from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM, AutoTokenizer
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

from app.config import CACHE_DIR

os.makedirs(CACHE_DIR, exist_ok=True)
file_utils.default_cache_path = CACHE_DIR

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_llm():
    model_checkpoints = {
        1: "defog/sqlcoder-7b-2", #AutoModelForCausalLM
        2: "defog/sqlcoder-70b-alpha", #AutoModelForCausalLM
        3: "premai-io/prem-1B-SQL", #AutoModelForCausalLM
        4: "chatdb/natural-sql-7b", #AutoModelForCausalLM
        5: "cssupport/t5-small-awesome-text-to-sql", #T5ForConditionalGeneration
    }
    
    model_checkpoint = model_checkpoints[5]
    print("Loading Model")
    try:
        model = T5ForConditionalGeneration.from_pretrained(model_checkpoint, cache_dir=CACHE_DIR).to(device)
        print("Model Loaded Successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    print("Loading Tokenizer")
    try:
        tokenizer = T5Tokenizer.from_pretrained('t5-small', cache_dir=CACHE_DIR)
        print("Tokenizer Loaded Successfully")
    except Exception as e:
        print(f"Error loading tokenizer: {e}")
        return None
    
    return model, tokenizer
