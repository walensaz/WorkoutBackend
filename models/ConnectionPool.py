import mysql.connector
from mysql.connector import pooling
import os

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class ConnectionPool(metaclass=Singleton):
    def __init__(self, pool_name="pool", pool_size=15):
        USER = os.getenv('USER')
        PASSWORD = os.getenv('PASSWORD')
        HOST = os.getenv('HOST')
        PORT = int(os.getenv('PORT'))
        dbconfig = {
            "user": USER,
            "password": PASSWORD,
            "host": HOST,
            "port": PORT,
            "database": "fitness_progress_tracker",
        }
        self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=pool_size, **dbconfig)

    def execute(self, query, params=None):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            # Pass the query and params to the execute method
            cursor.execute(query, params)
            # Fetch all the rows
            result = cursor.fetchall()
        except Exception as e:
            # Handle exceptions (e.g., log them, manage transaction if needed)
            print(f"Database execution error: {e}")
            result = None
        finally:
            # Ensure the connection is closed even if there is an error
            cnx.close()
        return result

