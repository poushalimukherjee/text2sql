import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.models.llm import load_llm
from app.tools.sql_executor import SQLExecutor
from app.services.text_to_sql_service import TextToSQLService
from app.prompts.prompt_templates import create_prompt
from app.config import DATABASE_DIR
from textwrap import dedent

llm, tokenizer = load_llm()
sql_executor = SQLExecutor()
text_to_sql_service = TextToSQLService(llm=llm, tokenizer=tokenizer, sql_executor=sql_executor)

app = FastAPI()

class QueryRequest(BaseModel):
    text: str  
class QueryResponse(BaseModel):
    PROMPT_INPUT: str  
    GENERATED_SQL_QUERY: str  
    QUERY_RESPONSE_FROM_DATABASE: list 


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        text_query = create_prompt(request.text)
        generated_query, results = text_to_sql_service.run(text_query)

        if results is None:
            raise HTTPException(status_code=400, detail="No results found or invalid query")
        return QueryResponse(PROMPT_INPUT=request.text, 
                             GENERATED_SQL_QUERY=generated_query, 
                             QUERY_RESPONSE_FROM_DATABASE=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.get("/")
async def root():
    return {"message": "Welcome to the Text-to-SQL API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
