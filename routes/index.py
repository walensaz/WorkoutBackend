from flask import render_template
from . import routes, connect

@routes.route('/')
def index():
    return {'message': 'Workout website API'}