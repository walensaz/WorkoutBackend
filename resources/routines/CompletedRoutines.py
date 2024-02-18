from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool
import calendar

from resources.utils.date_formatter import convert_date
from resources.utils.typescript_formatter import convert_keys

class CompletedRoutines(Resource):
    @jwt_required()
    def get(self):
        pool = ConnectionPool()
        email = get_jwt_identity().get('email')  # Extract user email from the JWT token
        year = request.args.get('year')
        month = request.args.get('month')
        
        # Validate the year and month parameters
        if not year:
            return {'message': 'Missing query parameter: year'}, 400
        if not month:
            return {'message': 'Missing query parameter: month'}, 400
        
        try:
            year = int(year)
            if (year < 1 or year > 9999):
                raise ValueError("Year must be between 1 and 9999")
            month = int(month)
            if month < 1 or month > 12:
                raise ValueError("Month must be between 1 and 12")
        except ValueError as e:
            return {'message': f'Invalid parameter values: {e}'}, 400
        
        # Calculate the last day of the month for the given year and month
        last_day = calendar.monthrange(year, month)[1]
        start_date = f"{year}-{month:02d}-01"
        end_date = f"{year}-{month:02d}-{last_day}"

        try:
            # Define the query
            query = """SELECT rl.routine_log_id, r.name, r.description, rl.date, rl.completion_status
                       FROM routine r
                       INNER JOIN routine_log rl ON r.routine_id = rl.routine_id
                       WHERE r.email = %s AND rl.date BETWEEN %s AND %s
                       ORDER BY rl.date DESC;"""
            # Execute the query with parameters
            result = pool.execute(query, (email, start_date, end_date))

            # Check for errors
            if result['message']:
                return {'message': result['message']}, 500

            # Check if there are rows returned
            if result['rows']:
                completed_routines = list(map(convert_date, convert_keys(result["rows"])))
                return completed_routines, 200
            else:
                return {'message': 'No completed routines found for the specified month and year'}, 404
        except Exception as e:
            return {'message': f'Error getting completed routines: {e}'}, 500
