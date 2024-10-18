from transformers import PreTrainedModel, PreTrainedTokenizer
from app.tools.sql_executor import SQLExecutor

class TextToSQLService:
    def __init__(self, llm: PreTrainedModel, tokenizer: PreTrainedTokenizer, sql_executor: SQLExecutor):
        self.llm = llm
        self.tokenizer = tokenizer
        self.sql_executor = sql_executor

    def create_prompt(self, text: str) -> str:
        return f"Convert the following text to an SQL query: {text}"

    def generate_sql(self, text: str) -> str:
        prompt = self.create_prompt(text)
        inputs = self.tokenizer(prompt, max_length=1024, return_tensors="pt")
        outputs = self.llm.generate(**inputs, max_new_tokens=1024)
        sql_query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return sql_query

    def run(self, text: str):
        sql_query = self.generate_sql(text)
        print(f"Generated SQL Query: {sql_query}")  # Print the generated SQL query
        try:
            return self.sql_executor.execute(sql_query)
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None
