from textwrap import dedent
from app.utils.extract_schema import extract_schema_ddl

# Extract schema information
schema_ddl = extract_schema_ddl()

def create_prompt(text: str) -> str:
    prompt_template = dedent(f'''\
            tables:\n{schema_ddl}\n\
            query for: {text}
            ''').strip()
    
    return prompt_template



