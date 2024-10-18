import os
from langchain_huggingface import HuggingFaceEndpoint
from transformers import file_utils 
from transformers import AutoModelForCausalLM, AutoModelForSeq2SeqLM
from transformers import  AutoTokenizer, T5Tokenizer
import torch
from app.config import HUGGINGFACE_API_KEY

base_dir = os.path.dirname(os.path.abspath(__file__))
cache_dir = os.path.join(base_dir, '../cache')
os.makedirs(cache_dir, exist_ok=True)

file_utils.default_cache_path = cache_dir

device = "cuda" if torch.cuda.is_available() else "cpu"

def load_llm():
    model_checkpoints = {
        1: "defog/sqlcoder-7b-2", #AutoModelForCausalLM
        2: "defog/sqlcoder-70b-alpha", #AutoModelForCausalLM
        3: "premai-io/prem-1B-SQL", #AutoModelForCausalLM
        4: "chatdb/natural-sql-7b", #AutoModelForCausalLM
        5: "cssupport/t5-small-awesome-text-to-sql", #AutoModelForSeq2SeqLM
        6: "gpt2"        
    }
    
    model_checkpoint = model_checkpoints[5]
    print("Loading Model")
    try:
        # model = AutoModelForCausalLM.from_pretrained(model_checkpoint, cache_dir=cache_dir).to(device)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint, cache_dir=cache_dir).to(device)
        print("Model Loaded Successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None

    print("Loading Tokenizer")
    try:
        # tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, cache_dir=cache_dir)
        tokenizer = T5Tokenizer.from_pretrained('t5-small')
        print("Tokenizer Loaded Successfully")
    except Exception as e:
        print(f"Error loading tokenizer: {e}")
        return None

    model_kwargs = {}
    print("Initializing HuggingFaceEndpoint")
    try:
        lang_model = HuggingFaceEndpoint(
            llm=model,
            repo_id=model_checkpoint,
            huggingfacehub_api_token=HUGGINGFACE_API_KEY,
            model_kwargs=model_kwargs,
            # device=device
        )
        print("HuggingFaceEndpoint Initialized Successfully")
    except Exception as e:
        print(f"Error initializing HuggingFaceEndpoint: {e}")
        return None

    return lang_model

# # from langchain_community.llms import PretrainedLLM
# # from langchain.llms import PretrainedLLM
# # from langchain import LangModel
# # from langchain import HuggingFaceHub
# import os
# # from langchain_community.llms import HuggingFaceHub
# from langchain_huggingface import HuggingFaceEndpoint
# from transformers import file_utils, AutoModelForCausalLM, AutoTokenizer
# import torch
# from app.config import HUGGINGFACE_API_KEY

# # Create a directory named 'cache' in the current directory
# base_dir = os.path.dirname(os.path.abspath(__file__))
# cache_dir = os.path.join(base_dir, '../cache')
# os.makedirs(cache_dir, exist_ok=True)

# # Set the cache directory globally
# file_utils.default_cache_path = cache_dir

# device = "cuda" if torch.cuda.is_available() else "cpu"

# def load_llm():
    
#     model_checkpoints = {
#         1: "defog/sqlcoder-7b-2",
#         2: "defog/sqlcoder-70b-alpha",
#         3: "premai-io/prem-1B-SQL",
#         4: "chatdb/natural-sql-7b",
#     }
    
#     model_checkpoint = model_checkpoints[1]
#     print("Loading Model")
#     model = AutoModelForCausalLM.from_pretrained(model_checkpoint, cache_dir=cache_dir)
#     print("Loaded Model 1")
#     # tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
#     print("Loaded Model")
#     print(model.generate())
#     model_kwargs={
#     #"temperature":0.00001
#               #    ,"return_full_text":False
#     }
#     lang_model = HuggingFaceEndpoint(
#         # repo_id=model_checkpoint,
#         llm = model,
#         repo_id=model_checkpoint,
#         huggingfacehub_api_token=HUGGINGFACE_API_KEY,
#         model_kwargs=model_kwargs,
#         # device=device
#     )
#     print("Loaded LLM")
#     return lang_model
