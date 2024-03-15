import base64
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from werkzeug.datastructures import FileStorage
from models.ConnectionPool import ConnectionPool

from resources.users.user_detail import UserDetail

class UserCRUD(Resource):
    @jwt_required()
    def put(self):
        pool = ConnectionPool()

        # Determine the content type
        content_type = request.content_type

        if content_type == 'application/json':
            data = request.get_json()
        elif 'multipart/form-data' in content_type:
            data = request.form.to_dict()  # Convert form data to dict
            avatar = request.files.get('avatar')
            if avatar and isinstance(avatar, FileStorage):
                data['avatar'] = avatar.read()  # Read as binary for BLOB storage
        else:
            return {"message": "Unsupported content type"}, 415

        # Extract data
        email = data.get("email", get_jwt_identity().get("email"))
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        visibility = data.get("visibility")

        age = int(data.get("age")) if data.get("age") else None
        gender = data.get("gender") if data.get("gender") else None
        bio = data.get("bio") if data.get("bio") else None
        avatar = data.get("avatar") if data.get("avatar") else None

        # Validation
        if not first_name:
            return {"message": "Missing field: firstName"}, 400
        if not last_name:
            return {"message": "Missing field: lastName"}, 400

        try:
            query = "SELECT * FROM user_profile WHERE email = %s;"
            result = pool.execute(query, (email,))

            if not result["rows"]:
                return {"message": "No user profile found to update"}, 404

            # Start constructing the update query
            update_query = """UPDATE user_profile SET first_name = %s, last_name = %s, age = %s, 
                              gender = %s, visibility = %s, bio = %s"""
            update_params = [first_name, last_name, age, gender, visibility, bio]

            # Append the avatar as a BLOB if it's provided
            if avatar:
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
