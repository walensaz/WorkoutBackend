import bcrypt
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Login(Resource):
    def post(self):
        pool = ConnectionPool()

        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email:
            return {'message': 'Missing field: email'}, 400
        if not password:
            return {'message': 'Missing field: password'}, 400
        
        query = "SELECT * FROM user WHERE Email = %s"
        result = pool.execute(query, (email,))

        if result['message']:
            return {'message': result['message']}, 500
        
        if result['rows']:
            password_hash = result['rows'][0]['password_hash']

            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                access_token = create_access_token(identity={"email": email}, expires_delta=timedelta(days=1))
                return {'token': access_token}, 200
            else:
                return {'message': 'Invalid credentials'}, 401
        else:
            return {'message': f'User with email {email} not found'}, 404
