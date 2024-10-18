import unittest
from app.models.llm import load_llm
from app.tools.sql_executor import SQLExecutor
from app.agents.text_to_sql_agent import TextToSQLAgent

class TestTextToSQLAgent(unittest.TestCase):
    def setUp(self):
        self.llm, self.tokenizer = load_llm()
        self.sql_executor = SQLExecutor()
        self.agent = TextToSQLAgent(llm=self.llm, tokenizer=self.tokenizer, sql_executor=self.sql_executor)

    def test_run(self):
        text_query = "Show all users who registered in the last month."
        results = self.agent.run(text_query)
        self.assertIsNotNone(results)

if __name__ == '__main__':
    unittest.main()

# import unittest
# from app.models.llm import load_llm
# from app.tools.sql_executor import SQLExecutor
# from app.agents.text_to_sql_agent import TextToSQLAgent

# if __name__ == '__main__':
#     unittest.main()

# class TestTextToSQLAgent(unittest.TestCase):
#     def setUp(self):
#         # self.llm = load_llm()
#         self.llm, self.tokenizer = load_llm()
#         self.sql_executor = SQLExecutor()
#         # self.agent = TextToSQLAgent(llm=self.llm, sql_executor=self.sql_executor)
#         self.agent = TextToSQLAgent(llm=self.llm, tokenizer=self.tokenizer, sql_executor=self.sql_executor)

#     def test_run(self):
#         print("Inside TestTextToSQLAgent.test_run")
#         text_query = "SELECT count(*) FROM IMDB"
#         results = self.agent.run(text_query)
#         self.assertIsNotNone(results)
#         print(results)

# if __name__ == '__main__':
#     unittest.main()
