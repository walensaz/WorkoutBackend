import bcrypt
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Register(Resource):
    def post(self):
        pool = ConnectionPool()

        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email:
            return {'message': 'Missing field: email'}, 400
        if not password:
            return {'message': 'Missing field: password'}, 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        query = "INSERT INTO user (email, password_hash) VALUES (%s, %s)"
        result = pool.execute(query, (email, hashed_password))

        if result['message']:
            return {'message': result['message']}, 500

        access_token = create_access_token(identity={"email": email}, expires_delta=timedelta(days=1))
        return {'token': access_token}, 200
