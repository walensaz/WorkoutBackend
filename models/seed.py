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

    create_user_table = """CREATE TABLE user (
                            user_id INT AUTO_INCREMENT PRIMARY KEY,
                            email VARCHAR(255) UNIQUE,
                            password_hash VARCHAR(255)
                        );"""
    pool.execute(create_user_table)

    create_user_profile_table = """CREATE TABLE user_profile (
                                profile_id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT,
                                first_name VARCHAR(255),
                                last_name VARCHAR(255),
                                age INT,
                                gender VARCHAR(50),
                                profile_visibility ENUM('PUBLIC', 'PRIVATE'),
                                bio TEXT,
                                avatar BLOB,
                                FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE
                            );"""
    pool.execute(create_user_profile_table)

    create_roles_table = """CREATE TABLE role (
                            role_id INT AUTO_INCREMENT PRIMARY KEY,
                            role_name VARCHAR(255)
                        );"""
    pool.execute(create_roles_table)

    create_user_roles_table = """CREATE TABLE user_role (
                              user_id INT,
                              role_id INT,
                              PRIMARY KEY (user_id, role_id),
                              FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
                              FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE CASCADE
                          );"""
    pool.execute(create_user_roles_table)

seed()
