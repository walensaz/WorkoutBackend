import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import ConnectionPool
from conftest import sqlResponse

def test_reset_password(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'UPDATE user SET password_hash = %s WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return {'rows': [{'email': 'dc@gmail.com', 'password_hash': '$2b$12$RF6JLXecIE4qujuPgTwkC.GN2BsOmGf8Ji10LyquoBaHkHWUWgiAm'}], 'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}
    ConnectionPool(testEffects=side_effects)

    test_password_mismatch(client)
    test_password_no_number(client)
    test_password_no_special_character(client)
    test_successful_password_reset(client)

def test_password_mismatch(client):
    # Test case: Passwords do not match
    response = client.post("/api/reset-password/token", json={
        'newPassword': 'Password1!',
        'confirmPassword': 'Password2!'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Passwords do not match'

def test_password_no_number(client):
    # Test case: Password does not have a number
    response = client.post("/api/reset-password/token", json={
        'newPassword': 'Password!',
        'confirmPassword': 'Password!'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Password must contain at least one number'

def test_password_no_special_character(client):
    # Test case: Password does not have a special character
    response = client.post("/api/reset-password/token", json={
        'newPassword': 'Password1',
        'confirmPassword': 'Password1'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Password must contain at least one special character'

def test_successful_password_reset(client):
    # Test case: Successful password reset
    response = client.post("/api/reset-password/token", json={
        'newPassword': 'Password1!',
        'confirmPassword': 'Password1!'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Password successfully updated'