from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool

class Users(Resource):
    def get(self):
        pool = ConnectionPool()
        query = "SELECT user_id, email FROM user"
        results = pool.execute(query)
        return {'users': results}, 200

class UserById(Resource):
    def get(self, user_id):
        pool = ConnectionPool()
        query = "SELECT user_id, email FROM user WHERE user_id = %s"
        results = pool.execute(query, (user_id,))
        if len(results) == 1:
            return {'users': results}, 200
        elif len(results) == 0:
            return {'message': f'User with UserID {user_id} not found'}, 404
        else:
            return {'message': 'Internal Server Error'}, 500


        

    

