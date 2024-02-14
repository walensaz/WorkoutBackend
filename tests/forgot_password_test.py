from models.ConnectionPool import ConnectionPool
from tests.conftest import app, client, sqlResponse

def test_forgot_password(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT email FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return {'rows': [('dc@gmail.com',)], 'message': ""}  # Indicates that the user exists
            elif args[1] == ('not.real@gmail.com',):
                return {'rows': [], 'message': ""}  # Indicates no such user, hence an empty array
            else:
                return {'rows': [], 'message': ""}  # Default case for other emails, also an empty array
        else:
            return {'rows': [], 'message': ""}

    ConnectionPool(testEffects=side_effects)
    # response = client.post("/api/login", json={""})
    # assert response.status_code == 400
    response = client.post("/api/forgot-password", json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"
    response = client.post("/api/forgot-password", json={'email': "not.real@gmail.com"})
    assert response.status_code == 200
 
    response = client.post("/api/forgot-password", json={'email': "dc@gmail.com"})
    assert response.json['message'] == "Password reset email sent to dc@gmail.com"
    assert response.status_code == 200