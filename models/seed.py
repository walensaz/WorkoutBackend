from ConnectionPool import ConnectionPool
from database import connect

def create_database():
    db_connection = connect()
    cursor = db_connection.cursor()
    cursor.execute("DROP DATABASE IF EXISTS fitness_progress_tracker;")
    cursor.execute("CREATE DATABASE fitness_progress_tracker;")
    db_connection.close()

def seed():
    create_database()

    pool = ConnectionPool()
    useDB = "USE fitness_progress_tracker;"
    pool.execute(useDB)

    createUserTable = """CREATE TABLE User (
                            UserID INT AUTO_INCREMENT PRIMARY KEY,
                            Email VARCHAR(255),
                            PasswordHash VARCHAR(255)
                        );"""
    pool.execute(createUserTable)

seed()