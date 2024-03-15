from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from resources.utils.typescript_formatter import convert_keys
import base64

class UserDetail(Resource):
    @jwt_required()
    def get(self):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')

        try:
            query_user_profile = """SELECT up.user_profile_id, up.first_name, up.last_name, up.age, 
                                    up.gender, up.visibility, up.bio, up.avatar
                                    FROM user_profile up
                                    WHERE up.email = %s;"""
            user_profile_result = pool.execute(query_user_profile, (email,))

            if not user_profile_result['rows']:
                return {'message': 'No user profile found for the specified email'}, 404

            user_profile = convert_keys(user_profile_result['rows'][0])
            
            # Converting the BLOB avatar to a base64 encoded string
            if user_profile.get('avatar'):
                avatar_blob = user_profile['avatar']
                user_profile['avatar'] = base64.b64encode(avatar_blob).decode('utf-8')

            # Fetching roles
            query_user_roles = """SELECT r.role_name
                                  FROM user_role ur
                                  INNER JOIN role r ON ur.role_id = r.role_id
                                  WHERE ur.email = %s;"""
            roles_result = pool.execute(query_user_roles, (email,))
            roles = [role['role_name'] for role in roles_result['rows']]
            user_profile['roles'] = roles

            if user_profile_result['message']:
                return {'message': user_profile_result['message']}, 500

            return user_profile, 200
        except Exception as e:
            return {'message': f'Error fetching user profile: {e}'}, 500
