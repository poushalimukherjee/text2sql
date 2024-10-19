import unittest
from app.models.llm import load_llm
from app.tools.sql_executor import SQLExecutor
from app.services.text_to_sql_service import TextToSQLService
from app.config import DATABASE_DIR
from textwrap import dedent


class TestTextToSQLService(unittest.TestCase):
    def setUp(self):
        self.llm, self.tokenizer = load_llm()
        self.sql_executor = SQLExecutor()
        self.service = TextToSQLService(llm=self.llm, tokenizer=self.tokenizer, sql_executor=self.sql_executor)

    def test_run(self):

        with open(f'{DATABASE_DIR}/schema_ddl.txt', 'r') as f:
            schema_string = f.read()

        text_query = dedent(f'''\
            tables:\n{schema_string}\n\
            query for: For IndianExpress group the rows by distinct dates and the count for each date.
            ''').strip()

        results = self.service.run(text_query)        
        self.assertIsNotNone(results)
        print(results)

if __name__ == '__main__':
    unittest.main()
