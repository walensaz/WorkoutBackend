from models.ConnectionPool import ConnectionPool

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
    # response = client.post("/api/login", json={""})
    # assert response.status_code == 400
    response = client.post("/api/forgot-password", json={})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"
    response = client.post("/api/forgot-password", json={'email': "dcd@gmail.com"})
    assert response.status_code == 201
    assert response.json['message'] == "Password reset email sent to dcd@gmail.com"
    response = client.post("/api/forgot-password", json={'email': "dc@gmail.com"})
    assert response.status_code == 500
    assert "Failed to send password reset email" in response.json['message']