import mysql.connector
import os
from unittest.mock import MagicMock

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    @classmethod
    def reset_instances(cls):
        cls._instances = {}


class ConnectionPool(metaclass=Singleton):
    def __init__(self, database="fitness_progress_tracker", pool_name="pool", pool_size=15, testEffects=None):
        USER = os.getenv('USER')
        PASSWORD = os.getenv('PASSWORD')
        HOST = os.getenv('HOST')
        PORT = int(os.getenv('PORT'))
        dbconfig = {
            "user": USER,
            "password": PASSWORD,
            "host": HOST,
            "port": PORT,
            "database": database,
        }

        if testEffects:
            self.cnxpool = MagicMock()
            self.execute = MagicMock(side_effect=testEffects)
        else:
            self.cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name=pool_name, pool_size=pool_size, **dbconfig)

    def execute(self, query, params=None):
        rows = None
        message = ""
        affected = 0
        last_insert_id = 0
        
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor(dictionary=True)

        try:
            # Pass the query and params to the execute method
            cursor.execute(query, params)
            if query.lower().startswith(("insert", "update", "delete")):
                if query.lower().startswith("insert"):
                    last_insert_id = cursor.lastrowid
                # Commit the transaction
                cnx.commit()
            # Fetch all the rows
            rows = cursor.fetchall()
            # return affected rows
            affected = cursor.rowcount
        except Exception as e:
            # Handle exceptions (e.g., log them, manage transaction if needed)
            message = f"Error: {e}"
        finally:
            # Ensure the connection is closed even if there is an error
            cnx.close()
        return {"rows": rows, "message": message, "affected": affected, "last_insert_id": last_insert_id}

