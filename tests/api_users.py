import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import ConnectionPool
from conftest import sqlResponse

def test_user(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT email FROM user':
            return sqlResponse(['dc@gmail.com', 'a@gmail.com'], "")
        elif args[0] == 'SELECT email FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return sqlResponse(['dc@gmail.com'], "")
            elif args[1] == ('a@gmail.com',):
                return sqlResponse(['a@gmail.com'], "")
            else:
                return sqlResponse([], "")
        else:
            return sqlResponse([], "")
    ConnectionPool(testEffects=side_effects)

    test_get_all_users(client)
    test_get_user_by_email(client)
    test_user_not_found(client)

def test_get_all_users(client):
    # Test case: Get all users
    response = client.get("/api/users/")
    json = response.json
    assert response.status_code == 200
    assert json['users'] == ['dc@gmail.com', 'a@gmail.com']

def test_get_user_by_email(client):
    # Test case: Get user by email
    response = client.get("/api/users/", query_string={"email": "dc@gmail.com"})
    json = response.json
    assert response.status_code == 200
    assert json['users'] == ['dc@gmail.com']

def test_user_not_found(client):
    # Test case: User not found
    response = client.get("/api/users/", query_string={"email": "dcd@gmail.com"})
    json = response.json
    assert response.status_code == 404
    assert json['message'] == "User with email dcd@gmail.com not found"