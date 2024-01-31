from flask import Flask, jsonify, request
from . import routes, extract_get

@routes.route('/workouts/user/', methods=['GET'])
def userWorkouts():
    userid, = extract_get(request)
    query = "SELECT * FROM workouts WHERE user = {}"
    return {'message': query.format(userid)}

@routes.route('/workouts/user/', methods=['POST'])
def testWorkouts():
    description = request.json['description']
    query = "SELECT * FROM workouts WHERE user = {}"
    return {'message': query.format(description)}
