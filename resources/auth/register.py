import bcrypt
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Register(Resource):
    def post(self):
        try:
            pool = ConnectionPool()

            email = request.json.get('email')
            password = request.json.get('password')
            
            if not email:
                return 'Missing email', 400
            if not password:
                return 'Missing password', 400
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            query = "INSERT INTO user (email, password_hash) VALUES (%s, %s)"
            pool.execute(query, (email, hashed_password))

            access_token = create_access_token(identity={"email": email}, expires_delta=timedelta(seconds=60))
            return {'access_token': access_token}, 200
        except Exception as e:
            return {'message': f'Error: {e}'}, 500
