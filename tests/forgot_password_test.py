import pytest
from models.ConnectionPool import ConnectionPool
from tests.conftest import app, client

@pytest.fixture
def mock_connection_pool(monkeypatch):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT email FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return {'rows': [('dc@gmail.com',)], 'message': ""}
            elif args[1] == ('not.real@gmail.com',):
                return {'rows': [], 'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}
    
    ConnectionPool(testEffects=side_effects)

def test_forgot_password_missing_field(client, mock_connection_pool):
    response = client.post("/api/forgot-password", json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"

def test_forgot_password_nonexistent_user(client, mock_connection_pool):
    response = client.post("/api/forgot-password", json={'email': "not.real@gmail.com"})
    assert response.status_code == 200

def test_forgot_password_existing_user(client, mock_connection_pool):
    response = client.post("/api/forgot-password", json={'email': "dc@gmail.com"})
    assert response.status_code == 200
    assert response.json['message'] == "Password reset email sent to dc@gmail.com"

