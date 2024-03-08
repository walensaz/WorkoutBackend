import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
from resources.utils.date_formatter import convert_date
from resources.utils.typescript_formatter import convert_keys
from resources.routines.routine_detail import RoutineDetail

class RoutineCRUD(Resource):
    @jwt_required()
    def get(self):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')

        try:
            query_routines = """SELECT routine_id, name, description, visibility, created 
                                FROM routine WHERE email = %s
                                ORDER BY created DESC;"""
            routines_result = pool.execute(query_routines, (email,))

            if not routines_result['rows']:
                return {'message': 'No routines found for the specified user'}, 404

            routines = list(map(convert_date, convert_keys(routines_result["rows"])))

            for routine in routines:
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
            
            if routines_result['message'] or exercises_result['message']:
                    return {'message': routines_result['message'] or exercises_result['message']}, 500

            return routines, 200
        except Exception as e:
            return {'message': f'Error fetching routines and their exercises: {e}'}, 500

    
    @jwt_required()
    def post(self):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email') 
        data = request.get_json()

        name = data.get('name')
        description = data.get('description')
        visibility = data.get('visibility')
        exercises = data.get('exercises')
        created = datetime.datetime.now().strftime('%Y-%m-%d')

        if not name:
            return {'message': 'Missing field: name'}, 400
        if not visibility:
            return {'message': 'Missing field: visibility'}, 400

        try:
            query = """INSERT INTO routine (email, name, description, visibility, created) 
                    VALUES (%s, %s, %s, %s, %s);"""
            result = pool.execute(query, (email, name, description, visibility, created))

            routine_id = result['last_insert_id']

            if exercises:
                for exercise in exercises:
                    if not exercise.get('exerciseId'):
                        return {'message': 'Missing field: exerciseId'}, 400
                    if not exercise.get('order') and exercise.get('order') != 0:
                        return {'message': 'Missing field: order'}, 400
                    if not exercise.get('repetitions'):
                        return {'message': 'Missing field: repetitions'}, 400
                    if not exercise.get('sets'):
                        return {'message': 'Missing field: sets'}, 400
                    if not exercise.get('restingTime'):
                        return {'message': 'Missing field: restingTime'}, 400

                    query = """INSERT INTO routine_exercise (routine_id, exercise_id, `order`, repetitions, sets, resting_time)
                            VALUES (%s, %s, %s, %s, %s, %s);"""

                    result = pool.execute(query, (
                        routine_id, 
                        exercise['exerciseId'], 
                        exercise['order'], 
                        exercise['repetitions'], 
                        exercise['sets'], 
                        exercise['restingTime']
                    ))

            if result['message']:
                return {'message': result['message']}, 500
        
            return RoutineDetail.get(self, routine_id)
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
        exercises = data.get('exercises')

        if not name:
            return {'message': 'Missing field: name'}, 400
        if not visibility:
            return {'message': 'Missing field:: visibility'}, 400

        try:
            query = "SELECT * FROM routine WHERE routine_id = %s AND email = %s;"
            result = pool.execute(query, (routine_id, email))

            if not result['rows']:
                return {'message': 'No routine found to update'}, 404
            
            query = """UPDATE routine SET name = %s, description = %s, visibility = %s
                    WHERE routine_id = %s AND email = %s;"""
            result = pool.execute(query, (name, description, visibility, routine_id, email))
            
            # The new exercises will replace the old ones and this allows the list to
            # include new exercises, remove old ones, and update existing ones.
            query = "DELETE FROM routine_exercise WHERE routine_id = %s;"
            result = pool.execute(query, (routine_id,))

            if exercises:
                for exercise in exercises:
                    if not exercise.get('exerciseId'):
                        return {'message': 'Missing field: exerciseId'}, 400
                    if not exercise.get('order') and exercise.get('order') != 0:
                        return {'message': 'Missing field: order'}, 400
                    if not exercise.get('repetitions'):
                        return {'message': 'Missing field: repetitions'}, 400
                    if not exercise.get('sets'):
                        return {'message': 'Missing field: sets'}, 400
                    if not exercise.get('restingTime'):
                        return {'message': 'Missing field: restingTime'}, 400
                    
                    query = """INSERT INTO routine_exercise (routine_id, exercise_id, `order`, repetitions, sets, resting_time)
                            VALUES (%s, %s, %s, %s, %s, %s);"""
                    
                    result = pool.execute(query, (
                        routine_id, 
                        exercise['exerciseId'], 
                        exercise['order'], 
                        exercise['repetitions'], 
                        exercise['sets'], 
                        exercise['restingTime']
                    ))
            
            if result['message']:
                return {'message': result['message']}, 500
            
            return RoutineDetail.get(self, routine_id)
        except Exception as e:
            return {'message': f'Error updating routine: {e}'}, 500


    @jwt_required()
    def delete(self, routine_id):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')

        routine = RoutineDetail.get(self, routine_id)

        try:
            query = "DELETE FROM routine WHERE routine_id = %s AND email = %s;"
            result = pool.execute(query, (routine_id, email))

            if result['affected'] == 0:
                return {'message': 'No routine found to delete'}, 404
            
            return routine
        except Exception as e:
            return {'message': f'Error deleting routine: {e}'}, 500
