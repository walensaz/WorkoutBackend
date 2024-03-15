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
    use_db = "USE fitness_progress_tracker;"
    pool.execute(use_db)

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
                                    visibility ENUM('PUBLIC', 'PRIVATE'),
                                    bio TEXT,
                                    avatar LONGBLOB,
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
                                role_id INT,
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
                                visibility ENUM('PUBLIC', 'PRIVATE'),
                                created DATE,
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
                                        completion_status BIT,
                                        FOREIGN KEY (routine_id) REFERENCES routine(routine_id) ON DELETE CASCADE
                                );"""
    pool.execute(create_routine_log_table)

    create_training_plan_table = """CREATE TABLE training_plan (
                                    plan_id INT AUTO_INCREMENT PRIMARY KEY,
                                    email VARCHAR(255),
                                    name VARCHAR(255),
                                    description TEXT,
                                    visibility ENUM('PUBLIC', 'PRIVATE'),
                                    created DATE,
                                    FOREIGN KEY (email) REFERENCES user(email) ON DELETE CASCADE
                                );"""
    pool.execute(create_training_plan_table)

    create_routine_training_plan_table = """CREATE TABLE routine_training_plan (
                                      id INT AUTO_INCREMENT PRIMARY KEY,
                                      plan_id INT,
                                      routine_id INT,
                                      planned_completion DATE,
                                      frequency ENUM('ONCE', 'DAILY', 'WEEKLY', 'BIWEEKLY', 'MONTHLY'),
                                      `order` INT,
                                      FOREIGN KEY (plan_id) REFERENCES training_plan(plan_id) ON DELETE CASCADE,
                                      FOREIGN KEY (routine_id) REFERENCES routine(routine_id) ON DELETE CASCADE
                                  );"""
    pool.execute(create_routine_training_plan_table)

    # Insert data
    add_excercises = """INSERT INTO exercise (name, description, category_type, body_part_focus, difficulty_level, equipment_needed) VALUES
                        ('Push-ups', 'Begin in a plank position with your hands slightly wider than shoulder-width apart and your body forming a straight line from head to heels. Lower your body until your chest nearly touches the floor, keeping your elbows close to your body. Push through your hands to return to the starting position. This exercise targets the chest, shoulders, and triceps, improving upper body strength and core stability.', 'Strength', 'Chest', 'Beginner', 'None'),
                        ('Squats', 'Stand with feet a bit wider than shoulder-width apart, toes pointing slightly outward. Bend your knees and lower your body as though sitting back into a chair, keeping your back straight and chest up. Lower down as far as possible, ideally until thighs are parallel to the floor, then push through your heels to return to standing. Squats target the quadriceps, hamstrings, glutes, and lower back, enhancing lower body strength and flexibility.', 'Strength', 'Legs', 'Beginner', 'None'),
                        ('Lunges', 'Start standing with your feet hip-width apart. Take a step forward with one leg and lower your hips until both knees are bent at about a 90-degree angle. The back knee should hover just above the ground, and the front knee should be directly over the ankle. Push back to the starting position. Lunges focus on the quads, hamstrings, glutes, and calves, improving balance and coordination.', 'Strength', 'Legs', 'Beginner', 'None'),
                        ('Plank', 'Assume a push-up position but with your forearms on the ground instead of your hands. Your elbows should be directly below your shoulders, and your body should form a straight line from your head to your feet. Hold this position, engaging your core, for a set amount of time. Planks strengthen the entire core, including the abs, obliques, and lower back.', 'Core', 'Abs', 'Beginner', 'None'),
                        ('Crunches', 'Lie on your back with knees bent and feet flat on the floor, hip-width apart. Place your hands behind your head without locking your fingers. Lift your upper body off the floor using your abdominal muscles, curling up towards your knees. Lower back down with control. Crunches primarily target the abdominal muscles, enhancing core strength.', 'Core', 'Abs', 'Beginner', 'None'),
                        ('Burpees', 'Start in a standing position, then drop into a squat with your hands on the ground. Kick your feet back into a plank position, perform a push-up, then quickly return your feet to the squat position. Leap up as high as possible from the squat position before returning to the starting position. Burpees are a full-body exercise that improves strength, endurance, and cardiovascular fitness.', 'Cardio', 'Full body', 'Intermediate', 'None'),
                        ('Deadlifts', 'Stand with feet hip-width apart, with a barbell in front of your shins. Bend at the hips and knees, gripping the bar with hands shoulder-width apart. Keeping your back straight, lift the bar by extending your hips and knees to full standing position. Lower the bar back to the ground under control. Deadlifts target the back, glutes, hamstrings, and core, enhancing overall strength and posture.', 'Strength', 'Back', 'Advanced', 'Barbell'),
                        ('Bench Press', 'Lie on a bench with your feet flat on the floor. Grip the barbell with hands just wider than shoulder-width apart. Lower the bar slowly until it touches your chest, then press the bar back up to the starting position. The bench press primarily targets the chest, shoulders, and triceps, improving upper body strength.', 'Strength', 'Chest', 'Intermediate', 'Barbell'),
                        ('Pull-ups', 'Grip a pull-up bar with hands slightly wider than shoulder-width apart, palms facing away from you. Pull your body up until your chin is above the bar, then lower back down with control. Pull-ups target the back, shoulders, and biceps, improving upper body strength and grip.', 'Strength', 'Back', 'Intermediate', 'Pull-up bar'),
                        ('Dips', 'Grip the parallel bars and hoist yourself up to a starting position with your arms fully extended and shoulders above your hands. Lower your body by bending your arms while leaning forward slightly, dipping down until your elbows are at a 90-degree angle. Push back up to the starting position. Dips target the triceps, chest, and shoulders, enhancing upper body strength.', 'Strength', 'Arms', 'Intermediate', 'Parallel bars'),
                        ('Bicep Curls', 'Stand with feet shoulder-width apart, holding a dumbbell in each hand at arm''s length. Curl the weights while keeping your upper arms stationary, exhale as you curl up, and inhale when lowering the dumbbells back.', 'Strength', 'Arms', 'Beginner', 'Dumbbell'),
                        ('Tricep Extensions', 'Stand with feet hip-width apart, holding a dumbbell with both hands above your head. Keep your elbows close to your ears and lower the weight behind your head, then extend your arms to lift the weight.', 'Strength', 'Arms', 'Beginner', 'Dumbbell'),
                        ('Shoulder Press', 'Sit or stand with feet shoulder-width apart, holding a dumbbell in each hand at shoulder height. Press the weights above your head until your arms are fully extended, then lower them back.', 'Strength', 'Shoulders', 'Intermediate', 'Dumbbell'),
                        ('Leg Press', 'Sit in a leg press machine with your back against the pad. Place your feet on the platform and push the weight up until your legs are extended, then return to the starting position.', 'Strength', 'Legs', 'Beginner', 'Leg press machine'),
                        ('Calf Raises', 'Stand with the balls of your feet on a raised surface with heels hanging off. Raise your heels as high as possible, then lower them below the platform level.', 'Strength', 'Calves', 'Beginner', 'None'),
                        ('Lat Pulldowns', 'Sit at a lat pulldown machine with knees secured. Grasp the bar with a wide grip and pull it down to chest level, then slowly release it back up.', 'Strength', 'Back', 'Beginner', 'Cable machine'),
                        ('Seated Rows', 'Sit at a cable row station with knees bent. Pull the handle towards your waist, keep your back straight, then slowly extend your arms back.', 'Strength', 'Back', 'Beginner', 'Cable machine'),
                        ('Leg Curls', 'Lie face down on a leg curl machine with legs extended. Curl your legs up towards your buttocks, then lower them back down.', 'Strength', 'Hamstrings', 'Beginner', 'Leg curl machine'),
                        ('Leg Extensions', 'Sit on a leg extension machine with legs under the pad. Lift the weight by extending your knees, then lower it back down.', 'Strength', 'Quadriceps', 'Beginner', 'Leg extension machine'),
                        ('Russian Twists', 'Sit on the floor with knees bent, lift your upper body and feet to create a V shape. Twist your torso to the sides, holding a weight for added resistance.', 'Core', 'Abs', 'Intermediate', 'Medicine ball'),
                        ('Mountain Climbers', 'Start in a plank position. Drive one knee towards your chest, then quickly switch legs, mimicking a running motion.', 'Cardio', 'Full body', 'Intermediate', 'None'),
                        ('Jump Rope', 'Hold a jump rope''s ends and swing it over your head and under your feet, jumping slightly to clear the rope each time.', 'Cardio', 'Full body', 'Beginner', 'Jump rope'),
                        ('Box Jumps', 'Face a sturdy box or platform. Perform a squat jump to land on the box, then step back down and repeat.', 'Plyometrics', 'Legs', 'Intermediate', 'Box'),
                        ('Kettlebell Swings', 'Stand with feet shoulder-width apart, holding a kettlebell with both hands. Swing the kettlebell between your legs and then up to chest height.', 'Strength', 'Full body', 'Intermediate', 'Kettlebell'),
                        ('Turkish Get-up', 'Lie on the floor holding a kettlebell in one hand with the arm fully extended. Rise to a standing position, keeping the kettlebell overhead, then reverse the motion.', 'Strength', 'Full body', 'Advanced', 'Kettlebell'),
                        ('Tuck Jumps', 'Stand with feet shoulder-width apart. Jump up, bringing your knees towards your chest at the peak of the jump, then land softly and repeat. Tuck jumps are a high-intensity exercise that improves explosive power and leg strength.', 'Plyometrics', 'Legs', 'Intermediate', 'None'),
                        ('Wall Sit', 'Slide your back down a wall until your thighs are parallel to the ground, with knees at a 90-degree angle, as if sitting in an invisible chair. Hold this position for time, strengthening the quadriceps, glutes, and calves.', 'Strength', 'Legs', 'Beginner', 'None'),
                        ('Flutter Kicks', 'Lie on your back with legs extended and hands under your buttocks. Lift your heels off the floor and make small, rapid up and down scissor-like motions with your legs, working the lower abdominal muscles.', 'Core', 'Abs', 'Beginner', 'None'),
                        ('High Knees', 'Run in place, lifting your knees high towards your chest. This exercise increases heart rate, improving cardiovascular fitness and leg strength.', 'Cardio', 'Full body', 'Beginner', 'None'),
                        ('Side Plank', 'Lie on your side with legs straight, propping your body up on one elbow and lifting your hips to form a straight line from head to feet. Hold this position to strengthen the obliques and improve core stability.', 'Core', 'Abs', 'Intermediate', 'None'),
                        ('Skull Crushers', 'Lie on a bench with a barbell, and extend your arms straight up. Lower the bar by bending your elbows, bringing it just above your forehead, then extend your arms to return to the starting position, targeting the triceps.', 'Strength', 'Arms', 'Intermediate', 'Barbell'),
                        ('Pendlay Rows', 'With a barbell on the ground, bend over it with your back parallel to the floor. Grip the barbell and row it towards your chest, keeping your torso stationary, then lower it back to the ground, targeting the upper back and lats.', 'Strength', 'Back', 'Advanced', 'Barbell'),
                        ('Hack Squat', 'Position yourself in a hack squat machine with your back against the pad. Bend your knees to lower your body, then press through your feet to return to the starting position, targeting the quadriceps, hamstrings, and glutes.', 'Strength', 'Legs', 'Intermediate', 'Hack squat machine'),
                        ('Farmer''s Walk', 'Hold a heavy weight in each hand and walk for a set distance or time. This exercise improves grip strength, core stability, and overall muscular endurance.', 'Strength', 'Full body', 'Intermediate', 'Heavy weights'),
                        ('Battle Ropes', 'Hold the ends of a battle rope with both hands, making waves by rapidly raising and lowering your arms. This exercise improves cardiovascular fitness, upper body strength, and endurance.', 'Cardio', 'Full body', 'Intermediate', 'Battle ropes'),
                        ('Chest Fly', 'Lie on a bench with dumbbells in each hand, arms extended above your chest. Lower the weights out to the sides of your body, then bring them back together above your chest, targeting the pectoral muscles for improved chest width and definition.', 'Strength', 'Chest', 'Intermediate', 'Dumbbell'),
                        ('Reverse Crunch', 'Lie on your back with hands at your sides or under your glutes. Lift your legs and bend your knees, then use your abs to pull your knees towards your chest, lifting your hips off the ground, targeting the lower abdominal muscles.', 'Core', 'Abs', 'Beginner', 'None'),
                        ('Step-ups', 'Stand in front of a bench or platform and step up onto it with one foot, pressing through your heel to lift your body up, then step back down and repeat, alternating legs, targeting the quadriceps, hamstrings, and glutes.', 'Strength', 'Legs', 'Beginner', 'Box'),
                        ('Thrusters', 'Hold a barbell at shoulder height, squat down, then stand and press the barbell overhead in one fluid motion, targeting the legs, core, and shoulders for improved overall strength and endurance.', 'Strength', 'Full body', 'Advanced', 'Barbell'),
                        ('Clean and Jerk', 'Lift a barbell from the ground to your shoulders (the clean), then from your shoulders to overhead (the jerk) in one fluid motion, improving explosive power, full-body strength, and coordination.', 'Olympic Weightlifting', 'Full body', 'Advanced', 'Barbell'),
                        ('Snatch', 'Lift a barbell from the ground directly to overhead in one smooth, continuous motion, requiring and developing explosive strength, power, and full-body coordination.', 'Olympic Weightlifting', 'Full body', 'Advanced', 'Barbell'),
                        ('Front Squat', 'With a barbell resting on your front shoulders, perform a squat, keeping your elbows up and maintaining a straight back, targeting the quadriceps and improving lower body strength and squat technique.', 'Strength', 'Legs', 'Intermediate', 'Barbell'),
                        ('Sumo Deadlift', 'Stand with feet wider than shoulder-width, gripping a barbell with hands inside your legs. Lift the bar by straightening your hips and knees, targeting the glutes, hamstrings, and inner thighs.', 'Strength', 'Legs', 'Intermediate', 'Barbell'),
                        ('Romanian Deadlift', 'Hold a barbell at hip level, lower it by moving your buttocks back with slightly bent knees, then lift it by extending your hips, targeting the hamstrings, glutes, and lower back.', 'Strength', 'Hamstrings', 'Intermediate', 'Barbell'),
                        ('Overhead Squat', 'With a barbell held overhead, perform a squat, requiring balance and flexibility while targeting the shoulders, hips, and core, along with the legs.', 'Strength', 'Legs', 'Advanced', 'Barbell'),
                        ('Hanging Leg Raise', 'Hang from a pull-up bar and raise your legs in front of you while keeping them straight, targeting the abdominal and hip flexor muscles for enhanced core strength and stability.', 'Core', 'Abs', 'Advanced', 'Pull-up bar'),
                        ('Dragon Flag', 'Lie on your back, lift your body off the bench to vertical using your shoulders as the pivot point, then lower yourself back down without your hips or lower back touching the bench, targeting the entire abdominal region.', 'Core', 'Abs', 'Advanced', 'None'),
                        ('Barbell Row', 'Bend over a barbell with a straight back and pull the bar towards your lower ribcage, then lower it back down, targeting the back muscles for improved strength and posture.', 'Strength', 'Back', 'Intermediate', 'Barbell'),
                        ('Goblet Squat', 'Hold a kettlebell close to your chest with both hands, perform a squat, targeting the quads, hamstrings, and glutes, and improving lower body strength and squatting technique.', 'Strength', 'Legs', 'Beginner', 'Kettlebell'),
                        ('Arnold Press', 'Sit with dumbbells at shoulder height, palms facing you. As you press the dumbbells overhead, rotate your hands so your palms face forward at the top, targeting multiple parts of the deltoids for improved shoulder strength and mobility.', 'Strength', 'Shoulders', 'Intermediate', 'Dumbbell');
                    """
    pool.execute(add_excercises)


seed()
