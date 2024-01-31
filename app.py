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
    db = {"connect": connect}

    # for routes usage
    # app.register_blueprint(routes)



    # API endpoints and the associated class.
    # For per class usage
    api.add_resource(resources.workouts.Workouts, '/workouts/user/')

    return app


if __name__ == '__main__':
    app = create_app()
    # app.run(debug=True, host="0.0.0.0")
    while True:
        try:
            app.run(host='0.0.0.0.', threaded=True, debug=True, port=5000)
        except Exception as e:
            print("It happened")
            time.sleep(5)
    # serve(app, host='0.0.0.0', port=5000)

