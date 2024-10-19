import unittest
from app.tools.sql_executor import SQLExecutor

class TestSQLExecutor(unittest.TestCase):
    def setUp(self):
        self.sql_executor = SQLExecutor()

    def test_execute(self):        
        queries = [
            "SELECT 1",
            "SELECT date, count(*) FROM IndianExpress GROUP BY date LIMIT 5",
            "SELECT min(date) FROM Telegraph"
        ]        
        for query in queries:
            results = self.sql_executor.execute(query)
            print(f'''QUERY: {query}\nRESULT:{results}\n\n''')                

if __name__ == '__main__':
    unittest.main()
