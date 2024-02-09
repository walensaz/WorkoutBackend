import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from flask_restful import Api
from flask_cors import CORS

import resources.auth.Login
import resources.auth.ForgotPassword
import resources.auth.ResetPassword
import resources.auth.Register
import resources.Users

from flask_mail import Mail
from resources.utils.email import send_email

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
    api.add_resource(resources.auth.Register.Register, '/register', '/register/')
    api.add_resource(resources.auth.Login.Login, '/login', '/login/')
    api.add_resource(resources.auth.ForgotPassword.ForgotPassword, '/forgot-password', '/forgot-password/')
    api.add_resource(resources.auth.ResetPassword.ResetPassword, '/reset-password/<token>', '/reset-password/<token>/')
    api.add_resource(resources.Users.Users, '/users','/users/')

    return app

if __name__ == '__main__':
    app = create_app()

    try:
        # Run the server on localhost + other configurations.
        app.run(host='localhost', threaded=True, debug=True, port=5000)
    except Exception as e:
        print(f"Error: {e}")


