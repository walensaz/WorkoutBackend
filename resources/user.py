from flask_restful import Resource, request
from models.ConnectionPool import ConnectionPool

class Users(Resource):
    def get(self):
        pool = ConnectionPool()
        query = "SELECT * FROM user"
        results = pool.execute(query)
        users = format_results(results)
        return {'users': users}, 200

class UserById(Resource):
    def get(self, user_id):
        pool = ConnectionPool()
        query = "SELECT * FROM user WHERE UserId = %s"
        results = pool.execute(query, (user_id,))
        users = format_results(results)
        if users and len(users) > 0:
            return {'users': users}, 200
        else:
            return {'error': f'User with UserID {user_id} not found'}, 404

def format_results(results):
    users = []
    for result in results:
        user = {
            'user_id': result[0],
            'email': result[1],
        }
        users.append(user)
    return users
        

    

