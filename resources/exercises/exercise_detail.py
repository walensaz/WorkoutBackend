from flask_restful import Resource
from models.ConnectionPool import ConnectionPool
from resources.utils.typescript_formatter import convert_keys


class ExerciseDetail(Resource):
    def get(self, exercise_id):
        pool = ConnectionPool()

        if not exercise_id:
            return {"message": "Missing route component: exercise_id"}, 400

        try:
            query = "SELECT * FROM exercise WHERE exercise_id = %s"
            result = pool.execute(query, (exercise_id,))

            if "rows" not in result or result["rows"] == 0:
                return {"message": f"No exercise with id {exercise_id} exists."}, 500

            if result["message"]:
                return {"message": result["message"]}, 500

            if result['rows']:
                completed_routines = convert_keys(result["rows"])[0]
                return completed_routines, 200
            else:
                return {'message': 'No completed routines found for the specified month and year'}, 404
            return convert_keys(result["rows"][0]), 200
        except Exception as e:
            return {"message": f"Failed. Error: {e}"}, 500
