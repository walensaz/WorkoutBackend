import pytest
from models.ConnectionPool import ConnectionPool
from tests.conftest import client, sqlResponse

@pytest.fixture
def mock_connection_pool_with_login(monkeypatch):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT * FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return sqlResponse([{'email': 'dc@gmail.com', 'password_hash': '$2b$12$2z2bCyIFSuCVcT/iGt1HNOUhxw7aSpR2MlrbbINzGMyhFIT.5rm9S'}], "")
            elif args[1] == ('a@gmail.com',):
                return sqlResponse([], "")  # Simulate no user found
            else:
                return sqlResponse([], "")  # No user found for other emails
        else:
            return sqlResponse([], "")  # Default case for non-matching queries
        
    ConnectionPool(testEffects=side_effects)

def test_login_missing_email_field(client, mock_connection_pool_with_login):
    response = client.post("/api/login", json={"password": "password"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"

def test_login_missing_password_field(client, mock_connection_pool_with_login):
    response = client.post("/api/login", json={"email": "dc@gmail.com"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: password"

def test_login_invalid_credentials(client, mock_connection_pool_with_login):
    # Test wrong password
    response = client.post("/api/login", json={'email': "dc@gmail.com", "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json['message'] == "Invalid credentials"
    # Test nonexistent email
    response = client.post("/api/login", json={'email': "nonexistent@gmail.com", "password": "password"})
    assert response.status_code == 401
    assert response.json['message'] == "Invalid credentials"

def test_login_successful(client, mock_connection_pool_with_login):
    response = client.post("/api/login", json={'email': "dc@gmail.com", "password": "Sachinfromgeekpython"})
    assert response.status_code == 200
    assert response.json['token'] is not None
