import unittest
from app.utils.extract_schema import extract_schema

class TestExtractSchema(unittest.TestCase):
    def test_extract_schema(self):
        # Extract schema information
        schema_info = extract_schema()

        # Check if the schema information is not empty
        self.assertTrue(schema_info.startswith("Tables:"))

        # Print the schema information in a well-formatted way
        print("Extracted Schema Information:")
        print(schema_info)
        
        # Save the schema information to a file
        with open("schema_info.txt", "w") as f:
            f.write(schema_info)
        
        print("Schema information saved to schema_info.txt")

if __name__ == '__main__':
    unittest.main()
