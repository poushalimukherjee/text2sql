from transformers import PreTrainedModel, PreTrainedTokenizer
from app.prompts.prompt_templates import create_prompt
from app.tools.sql_executor import SQLExecutor

class TextToSQLService:
    def __init__(self, llm: PreTrainedModel, tokenizer: PreTrainedTokenizer, sql_executor: SQLExecutor):
        self.llm = llm
        self.tokenizer = tokenizer
        self.sql_executor = sql_executor

    def create_prompt(self, text: str) -> str:
        return create_prompt(text)

    def generate_sql(self, text: str) -> str:
        prompt = self.create_prompt(text)
        inputs = self.tokenizer(prompt, max_length=1024, return_tensors="pt").to(self.llm.device)
        outputs = self.llm.generate(**inputs, max_new_tokens=1024)
        sql_query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return sql_query

    def run(self, text: str):
        sql_query = self.generate_sql(text)
        print(f"\nGenerated SQL Query:\n{sql_query}\n")
        try:
            print(f"Executing the generated Query:...")
            results = self.sql_executor.execute(sql_query)
            # Convert rows to dictionaries here
            formatted_results = [dict(row._mapping) for row in results]         

            return sql_query, formatted_results
        except Exception as e:
            print(f"Error executing SQL query: {e}")
            return None
