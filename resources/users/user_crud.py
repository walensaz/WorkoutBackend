from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
import base64

from resources.users.user_detail import UserDetail

class UserCRUD(Resource):
    @jwt_required()
    def put(self):
        pool = ConnectionPool()
        data = request.get_json()

        email = data.get("email")
        if not email:
            email = get_jwt_identity().get("email")

        first_name = data.get("first_name")
        last_name = data.get("last_name")
        age = data.get("age")
        gender = data.get("gender")
        visibility = data.get("visibility")
        bio = data.get("bio")
        avatar_encoded = data.get("avatar")  # Base64 encoded avatar

        if not first_name:
            return {"message": "Missing field: first_name"}, 400
        if not last_name:
            return {"message": "Missing field: last_name"}, 400

        try:
            query = "SELECT * FROM user_profile WHERE email = %s;"
            result = pool.execute(query, (email,))

            if not result["rows"]:
                return {"message": "No user profile found to update"}, 404

            # Start constructing the update query
            update_query = """UPDATE user_profile SET first_name = %s, last_name = %s, age = %s, 
                              gender = %s, visibility = %s, bio = %s"""
            update_params = [first_name, last_name, age, gender, visibility, bio]

            # Decode and append the avatar if it's provided
            if avatar_encoded:
                avatar = base64.b64decode(avatar_encoded)
                update_query += ", avatar = %s"
                update_params.append(avatar)

            # Finalize the update query and params
            update_query += " WHERE email = %s;"
            update_params.append(email)

            # Execute the update query
            pool.execute(update_query, tuple(update_params))

            if result["message"]:
                return {"message": result["message"]}, 500

            return UserDetail.get(self)
        except Exception as e:
            return {"message": f"Error updating user profile: {e}"}, 500
