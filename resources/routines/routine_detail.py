from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.ConnectionPool import ConnectionPool
from resources.utils.date_formatter import convert_date
from resources.utils.typescript_formatter import convert_keys

class RoutineDetail(Resource):
    @jwt_required()
    def get(self, routine_id):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')

        try:
            query_routine = """SELECT routine_id, name, description, visibility, created
                               FROM routine
                               WHERE email = %s AND routine_id = %s;"""
            routine_result = pool.execute(query_routine, (email, routine_id))

            if not routine_result['rows']:
                return {'message': 'No routine found for the specified ID'}, 404

            routine = convert_date(convert_keys(routine_result["rows"][0]))

            query_exercises = """SELECT re.routine_exercise_id, re.order, re.repetitions, re.sets, re.resting_time,
                                 e.exercise_id, e.name, e.description, e.category_type, 
                                 e.body_part_focus, e.difficulty_level, e.equipment_needed
                                 FROM routine_exercise re
                                 INNER JOIN exercise e ON re.exercise_id = e.exercise_id
                                 WHERE re.routine_id = %s
                                 ORDER BY re.order ASC;"""
            exercises_result = pool.execute(query_exercises, (routine['routineId'],))

            exercises = list(map(convert_date, convert_keys(exercises_result["rows"])))

            routine['exercises'] = exercises if exercises else []

            if routine_result['message']:
                return {'message': routine_result['message']}, 500

            return routine, 200
        except Exception as e:
            return {'message': f'Error fetching routine and its exercises: {e}'}, 500
