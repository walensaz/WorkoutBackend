import bcrypt
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Login(Resource):
    # login
    def post(self):
        pool = ConnectionPool()

        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        
        query = "SELECT * FROM user WHERE Email = %s"
        results = pool.execute(query, (email,))
        
        if len(results) == 1:
            user_id, hashed_password = results[0]
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                access_token = create_access_token(identity={"email": email}, expires_delta=timedelta(seconds=60))
                return {'access_token': access_token}, 200
            else:
                return {'message': 'Invalid credentials'}, 401
        elif len(results) == 0:
            return {'message': f'User with email {email} not found'}, 404
        else:
            return {'message': 'Internal Server Error'}, 500














    