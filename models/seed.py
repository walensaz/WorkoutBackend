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

    createUserTable = """CREATE TABLE user (
                            UserID INT AUTO_INCREMENT PRIMARY KEY,
                            Email VARCHAR(255) UNIQUE,
                            PasswordHash VARCHAR(255)
                        );"""
    pool.execute(createUserTable)

    createUserProfileTable = """CREATE TABLE user_profile (
                                ProfileID INT AUTO_INCREMENT PRIMARY KEY,
                                UserID INT,
                                FirstName VARCHAR(255),
                                LastName VARCHAR(255),
                                Age INT,
                                Gender VARCHAR(50),
                                ProfileVisibility ENUM('PUBLIC', 'PRIVATE'),
                                Bio TEXT,
                                Avatar BLOB,
                                FOREIGN KEY (UserID) REFERENCES user(UserID) ON DELETE CASCADE
                            );"""
    pool.execute(createUserProfileTable)

    createRolesTable = """CREATE TABLE role (
                            RoleID INT AUTO_INCREMENT PRIMARY KEY,
                            RoleName VARCHAR(255)
                        );"""
    pool.execute(createRolesTable)

    createUserRolesTable = """CREATE TABLE user_role (
                              UserID INT,
                              RoleID INT,
                              FOREIGN KEY (UserID) REFERENCES user(UserID) ON DELETE CASCADE,
                              FOREIGN KEY (RoleID) REFERENCES role(RoleID) ON DELETE CASCADE
                          );"""
    pool.execute(createUserRolesTable)

seed()
