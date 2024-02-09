import bcrypt
from flask_jwt_extended import decode_token
from flask_restful import Resource, request

from models.ConnectionPool import ConnectionPool

class ResetPassword(Resource):
    def post(self, token):
        new_password = request.json.get('newPassword')
        
        if not new_password:
            return {'message': 'Missing field: newPassword'}, 400
        
        try:
            # Decode the token manually to validate and extract information
            decoded_token = decode_token(token)
            user_email = decoded_token.get('sub', {}).get('email')

            if user_email:
                # Hash the new password
                hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())

                # Update the user's password in the database
                pool = ConnectionPool()
                query = "UPDATE user SET password_hash = %s WHERE email = %s"
                result = pool.execute(query, (hashed_password, user_email))

                if result['message']:
                    return {'message': result['message']}, 500

                return {'message': 'Password successfully updated'}, 200
            else:
                return {'message': 'Invalid or expired token'}, 401
        except Exception as e:
            # This will catch errors such as an expired token or tampering
            return {'message': f'Error updating password: {e}'}, 500