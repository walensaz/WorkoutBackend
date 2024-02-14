import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models import ConnectionPool

def test_forgot_password(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT COUNT(*) FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return {'rows': 1, 'message': ""}
            else:
                return {'rows': 0, 'message': ""}
        else:
            return {'rows': [], 'message': ""}
    ConnectionPool(testEffects=side_effects)

    test_missing_email_field(client)
    test_successful_email_sent(client)
    test_failed_email_sent(client)

def test_missing_email_field(client):
    # Test case: Missing email field
    response = client.post("/api/forgot-password", json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"

def test_successful_email_sent(client):
    # Test case: Successful email sent
    response = client.post("/api/forgot-password", json={'email': "dcd@gmail.com"})
    assert response.status_code == 201
    assert response.json['message'] == "Password reset email sent to dcd@gmail.com"

def test_failed_email_sent(client):
    # Test case: Failed email sent
    response = client.post("/api/forgot-password", json={'email': "dc@gmail.com"})
    assert response.status_code == 500
    assert "Failed to send password reset email" in response.json['message']