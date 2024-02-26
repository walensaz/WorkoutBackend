import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool

class ModifyRoutines(Resource):
    @jwt_required()
    def post(self):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email') 
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        visibility = data.get('visibility')
        created = datetime.datetime.now().strftime('%Y-%m-%d')

        if not name:
            return {'message': 'Missing field: name'}, 400
        if not description:
            return {'message': 'Missing field: description'}, 400
        if not visibility:
            return {'message': 'Missing field: visibility'}, 400

        try:
            query = """INSERT INTO routine (email, name, description, visibility, created) 
                    VALUES (%s, %s, %s, %s, %s);"""
            result = pool.execute(query, (email, name, description, visibility, created))

            if result['message']:
                return {'message': result['message']}, 500
            
            return {'message': 'Routine added successfully'}, 201
        except Exception as e:
            return {'message': f'Error adding routine: {e}'}, 500


    @jwt_required()
    def put(self, routine_id):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        visibility = data.get('visibility')

        if not name:
            return {'message': 'Missing field: name'}, 400
        if not description:
            return {'message': 'Missing field: description'}, 400
        if not visibility:
            return {'message': 'Missing field:: visibility'}, 400

        try:
            query = """UPDATE routine SET name = %s, description = %s, visibility = %s
                    WHERE routine_id = %s AND email = %s;"""
            result = pool.execute(query, (name, description, visibility, routine_id, email))

            if result['affected'] == 0:
                return {'message': 'No changes were made - ensure routine exists and new values have been provided'}, 500
            
            if result['message']:
                return {'message': result['message']}, 500
            
            return {'message': 'Routine updated successfully'}, 200
        except Exception as e:
            return {'message': f'Error updating routine: {e}'}, 500


    @jwt_required()
    def delete(self, routine_id):
        # Delete a routine
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')

        try:
            query = "DELETE FROM routine WHERE routine_id = %s AND email = %s;"
            result = pool.execute(query, (routine_id, email))

            if result['affected'] == 0:
                return {'message': 'No routine found to delete'}, 404
            
            return {'message': 'Routine deleted successfully'}, 200
        except Exception as e:
            return {'message': f'Error deleting routine: {e}'}, 500
