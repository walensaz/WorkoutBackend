import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from flask_restful import Api
from flask_cors import CORS

import resources.auth.login
import resources.auth.forgot_password
import resources.auth.reset_password
import resources.auth.register
import resources.users
import resources.exercises.exercise_crud
import resources.exercises.exercise_detail
import resources.routines.completed_routines
import resources.routines.routine_crud
import resources.routines.routine_detail

from flask_mail import Mail

from models.database import connect

def create_app():
    # Load env file
    load_dotenv()

    # Initialize Flask
    app = Flask(__name__)

    # Flask-Mail configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 465))
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

    # Secret key for JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

    # Initialize Flask-Mail
    app.mail = Mail(app)

    # Add JWTManager extension to the app
    jwt = JWTManager(app)

    # Add the API prefix to endpoints
    api = Api(app, prefix="/api")

    # Cross Origin Resource Sharing
    CORS(app)

    # Needed dict format to pass vars in add_resource
    db = {"connect": connect("fitness_progress_tracker")}

    # API endpoints and the associated class.
    # Allow '/' at the end of the endpoint.
    api.add_resource(
        resources.auth.register.Register, 
        '/register', 
        '/register/'
    )

    api.add_resource(
        resources.auth.login.Login, 
        '/login', 
        '/login/'
    )

    api.add_resource(
        resources.auth.forgot_password.ForgotPassword, 
        '/forgot-password', 
        '/forgot-password/'
    )

    api.add_resource(
        resources.auth.reset_password.ResetPassword, 
        '/reset-password/<token>', 
        '/reset-password/<token>/'
    )

    api.add_resource(
        resources.users.Users, 
        '/users',
        '/users/'
    )

    api.add_resource(
        resources.exercises.exercise_crud.ExerciseCRUD, 
        '/exercises', 
        '/exercises/'
    )

    api.add_resource(
        resources.exercises.exercise_detail.ExerciseDetail,
        '/exercise-details/<exercise_id>', 
        '/exercise-details/<exercise_id>/'
    )
    
    api.add_resource(
        resources.routines.completed_routines.CompletedRoutines, 
        '/completed-routines', 
        '/completed-routines/'
    )

    api.add_resource(
        resources.routines.routine_crud.RoutineCRUD, 
        '/routines', 
        '/routines/',
        '/routines/<routine_id>',
        '/routines/<routine_id1>/'
    )

    api.add_resource(
        resources.routines.routine_detail.RoutineDetail, 
        '/routine-details/<routine_id>', 
        '/routine-details/<routine_id>/'
    )

    return app

if __name__ == '__main__':
    app = create_app()

    try:
        # Run the server on localhost + other configurations.
        app.run(host='localhost', threaded=True, debug=True, port=5000)
    except Exception as e:
        print(f"Error: {e}")


