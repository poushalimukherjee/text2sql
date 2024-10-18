from langchain.prompts import PromptTemplate
from app.utils.extract_schema import extract_schema
# from app.config import database_path

# Extract schema information
schema_info = extract_schema()

prompt_template = PromptTemplate(
    template=f"""
    Given the following database schema:
    {schema_info}
    
    Convert the following text to an SQL query: {{text}}
    """,
    input_variables=["text"]
)
