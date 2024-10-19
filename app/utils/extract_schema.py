import os
import sqlite3
from app.config import database_path, DATABASE_URI, DATABASE_DIR

database_dir = DATABASE_DIR

print(f'''EXTRACTING SCHEMA FROM DATABASE_URI: {DATABASE_URI}''')

def extract_schema():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_info = "Tables:\n"

    for table in tables:
        table_name = table[0]
        schema_info += f"- {table_name}:\n"
        # Query to get column names and types for the table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        for col in columns:
            schema_info += f"    - {col[1]} ({col[2]})\n"

    conn.close()

    file_path = os.path.join(database_dir, 'schema_info.txt')
    with open(file_path, "w") as f:
        f.write(schema_info)
    print("Schema information saved to schema_info.txt")

    return schema_info

def extract_schema_ddl():
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table';")
    
    schemas = cursor.fetchall()
    schema_statements = []
    
    for schema in schemas:
        schema_statements.append(schema[0]+';')
    
    conn.close() 
    
    schema_string = "\n".join(schema_statements[0:])
    cleaned_schema_string = "\n".join([line for line in schema_string.splitlines() if line.strip()])

    file_path = os.path.join(database_dir, 'schema_ddl.txt')
    with open(file_path, "w") as f:
        f.write(cleaned_schema_string)
    print("Schema information saved to schema_ddl.txt")   
    
    return schema_string

