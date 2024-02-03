import os
import time

from dotenv import load_dotenv
from flask import Flask

from flask_restful import Api
from flask_cors import CORS

import resources.workouts
from models.database import connect
from routes import *

def create_app():
    # Load env file
    load_dotenv()

    # Initialize Flask
    app = Flask(__name__)
    # Ease of access for restful API
    api = Api(app)
    # Cross Origin Resource Sharing
    CORS(app)

    # Needed dict format to pass vars in add_resource
    db = {"connect": connect("fitness_progress_tracker")}

    # for routes usage
    # app.register_blueprint(routes)


    # API endpoints and the associated class.
    # For per class usage
    api.add_resource(resources.workouts.Workouts, '/api/users')

    return app


if __name__ == '__main__':
    app = create_app()
    try:
        # Run the server on localhost + other configurations.
        app.run(host='localhost', threaded=True, debug=True, port=5000)
    except Exception as e:
        print(f"Error: {e}")


