# %%
import os
from pathlib import Path
from transformers import AutoModelForSeq2SeqLM, T5Tokenizer, T5ForConditionalGeneration, AutoTokenizer, AutoModelForCausalLM
import torch
from sqlalchemy import create_engine, text

# %%
base_dir = Path(os.getcwd())
cache_dir = os.path.join(base_dir, './cache_alt')
os.makedirs(cache_dir, exist_ok=True)

# %%
base_dir

# %%
cache_dir

# %%
# Construct the full path to the SQLite database file
database_path = os.path.join(base_dir, '../databases/movie.sqlite')
# database_path = 'databases/movie.sqlite'
# Define the DATABASE_URI using the relative path
DATABASE_URI = f'sqlite:///{database_path}'
class SQLExecutor:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)

    def execute(self, query):
        print("DEBUG 1")
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()    

# %%
DATABASE_URI

# %%
sql_exec = SQLExecutor()

# %%
def test_execute(sql_exec):        
    queries = [
        "SELECT 1",
        "SELECT Title FROM IMDB",
        "SELECT count(Title) FROM IMDB"
    ]        
    for query in queries:
        results = sql_exec.execute(query)
        print(f'''QUERY: {query}\nRESULT:{results}\n\n''')        

# %%
test_execute(sql_exec)

# %% [markdown]
# #### Load Model

# %%
device = "cuda" if torch.cuda.is_available() else "cpu"

# %%
base_dir = Path(os.getcwd())
cache_dir = os.path.join(base_dir, './cache')

# %%
def load_llm():
    # model_checkpoint = "cssupport/t5-small-awesome-text-to-sql"
    model_checkpoint = "chatdb/natural-sql-7b"
    print("Loading Model")
    try:
        model = AutoModelForCausalLM.from_pretrained(model_checkpoint, cache_dir=cache_dir).to(device)
        print("Model Loaded Successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

    print("Loading Tokenizer")
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, cache_dir=cache_dir)
        print("Tokenizer Loaded Successfully")
    except Exception as e:
        print(f"Error loading tokenizer: {e}")
        return None, None

    return model, tokenizer

# %%
model, tokenizer = load_llm()

# %%
%%capture

model.to(device)
model.eval()

# %%
def generate_sql(input_prompt):
    # Tokenize the input prompt
    inputs = tokenizer(input_prompt, padding=True, truncation=True, return_tensors="pt").to(device)
    
    # Forward pass
    with torch.no_grad():
        outputs = model.generate(**inputs, max_length=512)
    
    # Decode the output IDs to a string (SQL query in this case)
    generated_sql = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return generated_sql

# %% [markdown]
# #### Test Model

# %%
# Define the path to the schema file
schema_file_path = os.path.join(base_dir.parent, 'schema_info.txt')

# Read the contents of the schema file
with open(schema_file_path, 'r') as file:
    schema_content = file.read()

print(schema_content)

# %%
prompt_00 = "tables:\n" + "CREATE TABLE student_course_attendance (student_id VARCHAR); \
    CREATE TABLE students (student_id VARCHAR)" + "\n" + "query for:" + \
    "List the id of students who never attends courses?"

# %%
prompt_00

# %%
prompt_01 = f'''\
tables:\n{schema_string}\n\
query for: List the unique movie titles in the database.
'''    

prompt_02 = f'''\
tables:\n{schema_string}\n\
query for: List each movie name and its genre from the database.
'''

# %%
prompt_01

# %%
generated_sql = generate_sql(prompt_02)

print(f"The generated SQL query is: {generated_sql}")

# %% [markdown]
# ### Read DB

# %%
import sqlite3

def extract_schema(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Query to get the schema creation statements
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    
    # Fetch all results
    schemas = cursor.fetchall()
    
    # Initialize an empty list to hold schema statements
    schema_statements = []
    
    # Print each schema creation statement and add to the list
    for schema in schemas:
        print(schema[0])
        schema_statements.append(schema[0])
    
    # Close the connection
    conn.close()
    
    # # Join the schema statements with newline characters, ignoring newline for the first element
    # if schema_statements:
    #     schema_string = schema_statements[0] + "\n" + "\n".join(schema_statements[1:])
    # else:
    #     schema_string = ""
    
    schema_string = "\n".join(schema_statements[0:])
    
    return schema_string

# Example usage
db_file = database_path
schema_string = extract_schema(db_file)
print("\nSchema String:\n", schema_string)

# %%
# Define the path to the output text file
output_file_path = os.path.join(base_dir.parent, 'db_file.txt')

# Write the value of db_file to the text file
with open(output_file_path, 'w') as file:
    file.write(extract_schema(db_file))

print(f"The value of db_file has been written to {output_file_path}")


