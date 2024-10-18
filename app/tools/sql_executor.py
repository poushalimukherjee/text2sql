# from sqlalchemy import create_engine
# from app.config import DATABASE_URI

# class SQLExecutor:
#     def __init__(self):
#         self.engine = create_engine(DATABASE_URI)

#     def execute(self, query):
#         with self.engine.connect() as connection:
#             result = connection.execute(query)
#             return result.fetchall()
        
from sqlalchemy import create_engine, text
from app.config import DATABASE_URI

class SQLExecutor:
    def __init__(self):
        self.engine = create_engine(DATABASE_URI)

    def execute(self, query):
        with self.engine.connect() as connection:
            result = connection.execute(text(query))
            return result.fetchall()        
