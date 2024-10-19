from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from app.config import DATABASE_URI     

class SQLExecutor:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI, pool_pre_ping=True)

    def execute(self, query):
        print(f"Inside SQLExecutor.execute...")
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(query))
                return result.fetchall()
        except OperationalError as oe:
            print(f"OperationalError: {oe}")
            raise
        except Exception as e:
            print(f"General SQL Execution Error: {e}")
            raise
