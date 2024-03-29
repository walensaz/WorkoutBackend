from flask_restful import Resource
from models.ConnectionPool import ConnectionPool
from resources.TypeScriptFormatter import convert_keys

class RoutineDetail(Resource):
    def get(self, routine_id):
        pool = ConnectionPool()

        if not routine_id:
            return {'message': 'Missing field: routine_id'}, 400

        try:
            query = ("SELECT routine_exercise.*, routine.name as routine_name, routine.description, exercise.name as exercise_name FROM routine_exercise "
                     "INNER JOIN routine ON routine_exercise.routine_id = routine.routine_id "
                     "INNER JOIN exercise ON routine_exercise.exercise_id = exercise.exercise_id "
                     "WHERE routine_exercise.routine_id = %s")
            result = pool.execute(query, (routine_id,))

            if 'rows' not in result or result['rows'] == 0:
                return {'message': f'No routine with id {routine_id} exists.'}, 500

            if result['message']:
                return {'message': result['message']}, 500

            return convert_keys(result["rows"]), 200
        except Exception as e:
            return {'message': f'Failed. Error: {e}'}, 500