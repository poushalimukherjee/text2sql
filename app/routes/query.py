from flask import Blueprint, request, jsonify
from app.models.llm import load_llm
from app.tools.sql_executor import SQLExecutor
from app.agents.text_to_sql_agent import TextToSQLAgent

query_blueprint = Blueprint('query', __name__)

llm = load_llm()
sql_executor = SQLExecutor()
agent = TextToSQLAgent(llm, sql_executor)

@query_blueprint.route('/query', methods=['POST'])
def query():
    text = request.json.get('text')
    results = agent.run(text)
    return jsonify(results)
