from flask_restful import Resource
from models.ConnectionPool import ConnectionPool
from resources.utils.typescript_formatter import convert_keys

class ExerciseCRUD(Resource):
    def get(self):
        pool = ConnectionPool()

        try:
            query = "SELECT * FROM exercise"
            result = pool.execute(query)

            if 'rows' not in result or result['rows'] == 0:
                return {'message': 'No exercises found.'}, 404

            # Convert keys for each exercise in the result set
            exercises = list(convert_keys(result["rows"]))

            return exercises, 200
        except Exception as e:
            return {'message': f'Failed. Error: {e}'}, 500
