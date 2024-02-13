import bcrypt
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from flask_jwt_extended import create_access_token
from datetime import timedelta

class Register(Resource):
    def post(self):
        pool = ConnectionPool()

        first_name = request.json.get('firstName')
        last_name = request.json.get('lastName')
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not first_name:
            return {'message': 'Missing field: firstName'}, 400
        if not last_name:
            return {'message': 'Missing field: lastName'}, 400
        if not email:
            return {'message': 'Missing field: email'}, 400
        if not password:
            return {'message': 'Missing field: password'}, 400
        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Insert into user table
        user_insert_query = "INSERT INTO user (email, password_hash) VALUES (%s, %s)"
        user_result = pool.execute(user_insert_query, (email, hashed_password))

        if user_result['message']:
            return {'message': user_result['message']}, 500

        # Insert into user_profile table
        profile_insert_query = "INSERT INTO user_profile (email, first_name, last_name) VALUES (%s, %s, %s)"
        profile_result = pool.execute(profile_insert_query, (email, first_name, last_name))

        if profile_result['message']: 
            return {'message': profile_result['message']}, 500

        access_token = create_access_token(identity={"email": email}, expires_delta=timedelta(days=1))
        return {'token': access_token}, 200
