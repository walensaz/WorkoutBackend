import os
import mysql.connector as mysql

def connect(database=None):
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))

    connection_params = {
        'user': USER,
        'password': PASSWORD,
        'host': HOST,
        'port': PORT
    }

    # Optionally connect to a specific database
    if database:
        connection_params['database'] = database

    try:
        return mysql.connect(**connection_params)
    except mysql.Error as e:
        print(f"Error connecting to MYSQL: {e}")
        return
