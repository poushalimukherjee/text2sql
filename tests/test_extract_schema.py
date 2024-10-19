import unittest
from app.utils.extract_schema import extract_schema, extract_schema_ddl

class TestExtractSchema(unittest.TestCase):
    def test_extract_schema(self):
        # Extract schema information
        schema_info = extract_schema()
        schema_ddl = extract_schema_ddl()

        # Check if the schema information is not empty
        self.assertTrue(schema_info.startswith("Tables:"))
        self.assertTrue(schema_ddl.startswith("CREATE TABLE"))

        # Print the schema information in a well-formatted way
        print("Extracted Schema Information:")
        print(schema_info)
        print('Extracted Schema DDL:')
        print(schema_ddl)

if __name__ == '__main__':
    unittest.main()
