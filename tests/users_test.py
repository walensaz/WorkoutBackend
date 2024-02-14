import pytest
from models.ConnectionPool import ConnectionPool
from tests.conftest import app, client, execute_side_effects, sqlResponse

@pytest.fixture
def mock_connection_pool_with_users(monkeypatch):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT email FROM user':
            return sqlResponse(['dc@gmail.com', 'a@gmail.com'], "")
        elif args[0] == 'SELECT email FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return sqlResponse(['dc@gmail.com'], "")
            elif args[1] == ('a@gmail.com',):
                return sqlResponse(['a@gmail.com'], "")
            else:
                return sqlResponse([], "")  # Simulate no user found for other emails
        else:
            return sqlResponse([], "")  # Default case for non-matching queries
        
    ConnectionPool(testEffects=side_effects)

def test_get_all_users(client, mock_connection_pool_with_users):
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert response.json['users'] == ['dc@gmail.com', 'a@gmail.com']

def test_get_user_by_email_exists(client, mock_connection_pool_with_users):
    response = client.get("/api/users/", query_string={"email": "dc@gmail.com"})
    assert response.status_code == 200
    assert response.json['users'] == ['dc@gmail.com']

def test_get_user_by_email_not_found(client, mock_connection_pool_with_users):
    response = client.get("/api/users/", query_string={"email": "dcd@gmail.com"})
    assert response.status_code == 404
    assert response.json['message'] == "User with email dcd@gmail.com not found"
