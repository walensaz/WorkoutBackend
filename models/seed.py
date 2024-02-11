from ConnectionPool import ConnectionPool
from database import connect
from dotenv import load_dotenv

def create_database():
    load_dotenv()

    try:
        db_connection = connect()
        cursor = db_connection.cursor()
        cursor.execute("DROP DATABASE IF EXISTS fitness_progress_tracker;")
        cursor.execute("CREATE DATABASE fitness_progress_tracker;")
    except Exception as e:
        print(f"Error creating database: {e}")
    finally:
        db_connection.close()

def seed():
    create_database()

    pool = ConnectionPool()
    useDB = "USE fitness_progress_tracker;"
    pool.execute(useDB)

    # Create tables
    create_user_table = """CREATE TABLE user (
                            email VARCHAR(255) PRIMARY KEY,
                            password_hash VARCHAR(255)
                        );"""
    pool.execute(create_user_table)

    create_user_profile_table = """CREATE TABLE user_profile (
                                user_profile_id INT AUTO_INCREMENT PRIMARY KEY,
                                email VARCHAR(255),
                                first_name VARCHAR(255),
                                last_name VARCHAR(255),
                                age INT,
                                gender VARCHAR(50),
                                profile_visibility ENUM('PUBLIC', 'PRIVATE'),
                                bio TEXT,
                                avatar BLOB,
                                FOREIGN KEY (email) REFERENCES user(email) ON DELETE CASCADE
                            );"""
    pool.execute(create_user_profile_table)

    create_roles_table = """CREATE TABLE role (
                            role_id INT AUTO_INCREMENT PRIMARY KEY,
                            role_name VARCHAR(255)
                        );"""
    pool.execute(create_roles_table)

    create_user_roles_table = """CREATE TABLE user_role (
                              user_role_id INT AUTO_INCREMENT PRIMARY KEY,
                              email VARCHAR(255),
                              FOREIGN KEY (email) REFERENCES user(email) ON DELETE CASCADE,
                              FOREIGN KEY (role_id) REFERENCES role(role_id) ON DELETE CASCADE
                          );"""
    pool.execute(create_user_roles_table)

    create_exercise_table = """CREATE TABLE exercise (
                                exercise_id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                description TEXT,
                                category_type VARCHAR(255),
                                body_part_focus VARCHAR(255),
                                difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced'),
                                equipment_needed VARCHAR(255)
                            );"""
    pool.execute(create_exercise_table)

    create_routine_table = """CREATE TABLE routine (
                                    routine_id INT AUTO_INCREMENT PRIMARY KEY,
                                    email VARCHAR(255),
                                    name VARCHAR(255),
                                    description TEXT,
                                    FOREIGN KEY (email) REFERENCES user(email) ON DELETE CASCADE
                                );"""
    pool.execute(create_routine_table)

    create_routine_exercise_table = """CREATE TABLE routine_exercise (
                                            routine_exercise_id INT AUTO_INCREMENT PRIMARY KEY,
                                            routine_id INT,
                                            exercise_id INT,
                                            `order` INT,
                                            repetitions INT,
                                            sets INT,
                                            resting_time INT,
                                            FOREIGN KEY (routine_id) REFERENCES routine(routine_id) ON DELETE CASCADE,
                                            FOREIGN KEY (exercise_id) REFERENCES exercise(exercise_id) ON DELETE CASCADE
                                        );"""
    pool.execute(create_routine_exercise_table)

    create_routine_log_table = """CREATE TABLE routine_log (
                                        routine_log_id INT AUTO_INCREMENT PRIMARY KEY,
                                        routine_id INT,
                                        date DATE,
                                        completion_status VARCHAR(255),
                                        FOREIGN KEY (routine_id) REFERENCES routine(routine_id) ON DELETE CASCADE
                                    );"""
    pool.execute(create_routine_log_table)

seed()
