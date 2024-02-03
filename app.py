import os
import time

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager

from flask_restful import Api
from flask_cors import CORS

import resources.auth.login
import resources.auth.register
import resources.user

from models.database import connect

def create_app():
    # Load env file
    load_dotenv()

    # Initialize Flask
    app = Flask(__name__)
    # Secret key for JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
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
    api.add_resource(resources.auth.register.Register, '/register', '/register/')
    api.add_resource(resources.auth.login.Login, '/login', '/login/')
    api.add_resource(resources.user.Users, '/users','/users/')
    api.add_resource(resources.user.UserById, '/users/<int:user_id>','/users/<int:user_id>/')

    return app


if __name__ == '__main__':
    app = create_app()
    try:
        # Run the server on localhost + other configurations.
        app.run(host='localhost', threaded=True, debug=True, port=5000)
    except Exception as e:
        print(f"Error: {e}")


