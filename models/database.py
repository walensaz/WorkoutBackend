import os
import mysql.connector as mysql

def connect():
    USER = os.getenv('USER')
    PASSWORD = os.getenv('PASSWORD')
    HOST = os.getenv('HOST')
    PORT = int(os.getenv('PORT'))

    # Connect to MYSQL
    try:
        return mysql.connect(
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT,
            database="workout_app"
        )
    except mysql.Error as e:
        print(f"Error connecting to MYSQL: {e}")