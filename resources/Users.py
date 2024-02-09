from flask_jwt_extended import jwt_required
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool

class Users(Resource):
    def get(self):
        pool = ConnectionPool()

        email = request.args.get('email')
        
        if email: # If email is not None, then we want to get the user with that email
            query = "SELECT email FROM user WHERE email = %s"
            result = pool.execute(query, (email,))

            if result['message']:
                return {'message': result['message']}, 500

            if result['rows']:
                return {'users': result["rows"]}, 200
            else:
                return {'message': f'User with email {email} not found'}, 404
        else: # If email is None, then we want to get all the users
            query = "SELECT email FROM user"
            result = pool.execute(query)

            if result['message']:
                return {'message': result['message']}, 500

            return {'users': result["rows"]}, 200
