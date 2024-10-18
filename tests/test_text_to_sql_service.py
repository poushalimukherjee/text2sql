import unittest
from app.models.llm import load_llm
from app.tools.sql_executor import SQLExecutor
from app.services.text_to_sql_service import TextToSQLService

class TestTextToSQLService(unittest.TestCase):
    def setUp(self):
        self.llm, self.tokenizer = load_llm()
        self.sql_executor = SQLExecutor()
        self.service = TextToSQLService(llm=self.llm, tokenizer=self.tokenizer, sql_executor=self.sql_executor)

    def test_run(self):
        text_query = "Show all users who registered in the last month."
        results = self.service.run(text_query)
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()
