# import sqlite3
# from app.config import database_path

# def extract_schema():
#     # Connect to the SQLite database
#     conn = sqlite3.connect(database_path)
#     cursor = conn.cursor()

#     # Query to get all table names
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()

#     schema_info = "Tables:\n"

#     for table in tables:
#         table_name = table[0]
#         schema_info += f"- {table_name}: "

#         # Query to get column names and types for the table
#         cursor.execute(f"PRAGMA table_info({table_name});")
#         columns = cursor.fetchall()

#         column_info = ", ".join([f"{col[1]} ({col[2]})" for col in columns])
#         schema_info += f"{column_info}\n"

#     # Close the connection
#     conn.close()

#     return schema_info

# if __name__ == "__main__":
#     schema_info = extract_schema()
#     print(schema_info)

import sqlite3
from app.config import database_path

def extract_schema():
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Query to get all table names
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

    # Close the connection
    conn.close()

    return schema_info

if __name__ == "__main__":
    schema_info = extract_schema()
    print(schema_info)
