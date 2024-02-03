from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool

class Users(Resource):
    def get(self):
        pool = ConnectionPool()

        query = "SELECT user_id, email FROM user"
        result = pool.execute(query)

        if result['message']:
            return {'message': result['message']}, 500
        
        return {'users': result["rows"]}, 200

class UserById(Resource):
    def get(self, user_id):
        pool = ConnectionPool()

        query = "SELECT user_id, email FROM user WHERE user_id = %s"
        result = pool.execute(query, (user_id,))

        if result['message']:
            return {'message': result['message']}, 500
        
        if result['rows']:
            return {'users': result["rows"]}, 200
        else:
            return {'message': f'User with UserID {user_id} not found'}, 404

        

    

