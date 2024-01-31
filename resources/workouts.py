from flask_restful import Resource, Api, request
from flask import jsonify
from models.ConnectionPool import ConnectionPool

class Workouts(Resource):
    def __init__(self) -> None:
        super().__init__()

    def get(self) -> dict:
        pool = ConnectionPool()
        query = "SELECT * FROM workouts WHERE user = {}"
        pool.execute(query)
        return {'message': query.format(request.args.get('userid'))}

    def post(self) -> dict:
        description = request.json['description']
        query = "SELECT * FROM workouts WHERE user = {}"
        return {'message': query.format(description)}
