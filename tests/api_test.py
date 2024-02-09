from models.ConnectionPool import ConnectionPool

def sqlResponse(rows, message):
    return {'rows': rows, 'message': message}

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
    response = client.get("/api/users/")
    json = response.json
    assert json['users'] == ['dc@gmail.com', 'a@gmail.com']
    response = client.get("/api/users/", query_string={"email": "dc@gmail.com"})
    json = response.json
    assert response.status_code == 200
    assert json['users'] == ['dc@gmail.com']
    response = client.get("/api/users/", query_string={"email": "dcd@gmail.com"})
    json = response.json
    assert json['message'] == "User with email dcd@gmail.com not found"
    assert response.status_code == 404

def test_login(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT * FROM user WHERE Email = %s':
            if args[1] == ('dc@gmail.com',):
                return sqlResponse([{'email': 'dc@gmail.com', 'password_hash': '$2b$12$RF6JLXecIE4qujuPgTwkC.GN2BsOmGf8Ji10LyquoBaHkHWUWgiAm'}], "")
            elif args[1] == ('a@gmail.com',):
                return {'rows': ['a@gmail.com'], 'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}
    ConnectionPool(testEffects=side_effects)
    # response = client.post("/api/login", json={""})
    # assert response.status_code == 400
    response = client.post("/api/login", json={"email": "dc@gmail.com"})
    assert response.status_code == 400
    response = client.post("/api/login", json={"password": "password"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"
    response = client.post("/api/login", json={'email': "dc@gmail.com", "password": "password"})
    assert response.status_code == 401
    assert response.json['message'] == "Invalid credentials"
    response = client.post("/api/login", json={'email': "dc@gmail.com", "password": "Sachinfromgeekpython"})
    assert response.status_code == 200
    assert response.json['access_token'] is not None

def test_register(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'INSERT INTO user (email, password_hash) VALUES (%s, %s)':
            if args[1] == ('dc@gmail.com',):
                return {'rows': [{'email': 'dc@gmail.com', 'password_hash': '$2b$12$RF6JLXecIE4qujuPgTwkC.GN2BsOmGf8Ji10LyquoBaHkHWUWgiAm'}], 'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}
    ConnectionPool(testEffects=side_effects)
    # response = client.post("/api/login", json={""})
    # assert response.status_code == 400
    response = client.post("/api/register", json={"email": "dc@gmail.com"})
    assert response.status_code == 400
    response = client.post("/api/register", json={"password": "password"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"
    response = client.post("/api/register", json={'email': "dc@gmail.com", "password": "Sachinfromgeekpython"})
    assert response.status_code == 200
    assert response.json['access_token'] is not None

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

