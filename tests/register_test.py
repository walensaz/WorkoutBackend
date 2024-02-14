import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import ConnectionPool
from conftest import sqlResponse
import pytest
from models.ConnectionPool import ConnectionPool
from tests.conftest import app, client

@pytest.fixture
def mock_connection_pool(monkeypatch):
    def side_effects(*args, **kwargs):
        if args[0] == 'INSERT INTO user (email, password_hash) VALUES (%s, %s)':
            if args[1] == ('dc@gmail.com',):
                return {'rows': [{'email': 'dc@gmail.com', 'password_hash': '$2b$12$RF6JLXecIE4qujuPgTwkC.GN2BsOmGf8Ji10LyquoBaHkHWUWgiAm'}], 'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}

    ConnectionPool(testEffects=side_effects)

def test_register_missing_email(client, mock_connection_pool):
    response = client.post("/api/register", json={"firstName": "Zach", "lastName": "Wal", "password": "password"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"

def test_register_missing_other_fields(client, mock_connection_pool):
    # Example for missing password, similar tests can be added for other fields
    response = client.post("/api/register", json={"email": "dc@gmail.com", "firstName": "Zach", "lastName": "Wal"})
    assert response.status_code == 400
    # Assuming the API returns a general message for missing fields
    assert "Missing field" in response.json['message']

def test_register_successful(client, mock_connection_pool):
    response = client.post("/api/register", json={"firstName": "Zach", "lastName": "Wal", 'email': "dc@gmail.com", "password": "Sachinfromgeekpython"})
    assert response.status_code == 200
    assert response.json['token'] is not None
