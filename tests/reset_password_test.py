import datetime
import os
import sys

import pytest
from flask_jwt_extended import create_access_token
from models.ConnectionPool import ConnectionPool

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def mock_connection_pool(monkeypatch):
    def side_effects(*args, **kwargs):
        if args[0] == 'UPDATE user SET password_hash = %s WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return {'rows': [{'email': 'dc@gmail.com',
                                  'password_hash': '$2b$12$RF6JLXecIE4qujuPgTwkC.GN2BsOmGf8Ji10LyquoBaHkHWUWgiAm'}],
                        'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}

    ConnectionPool(testEffects=side_effects)


def gen_token(email, expire_time=datetime.timedelta(hours=1)):
    reset_token = create_access_token(identity=email, expires_delta=expire_time)
    return reset_token

def test_password_mismatch(app, client, mock_connection_pool):
    with app.app_context():
        token = gen_token(email='dc@gmail.com')
    # Test case: Passwords do not match
    response = client.post("/api/reset-password/" + token, json={
        'newPassword': 'Password1!',
        'confirmPassword': 'Password2!'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Passwords do not match'

def test_password_no_number(app, client, mock_connection_pool):
    with app.app_context():
        token = gen_token(email='dc@gmail.com')
    # Test case: Password does not have a number
    response = client.post("/api/reset-password/" + token, json={
        'newPassword': 'Password!',
        'confirmPassword': 'Password!'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Password must contain at least one number'

def test_password_no_special_character(app, client, mock_connection_pool):
    with app.app_context():
        token = gen_token(email='dc@gmail.com')
    # Test case: Password does not have a special character
    response = client.post("/api/reset-password/" + token, json={
        'newPassword': 'Password1',
        'confirmPassword': 'Password1'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Password must contain at least one special character'

def test_successful_password_reset(app, client, mock_connection_pool):
    with app.app_context():
        token = gen_token(email='dc@gmail.com')
    # Test case: Successful password reset
    response = client.post("/api/reset-password/" + token, json={
        'newPassword': 'Password1!',
        'confirmPassword': 'Password1!'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Password successfully updated'