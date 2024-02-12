from models.ConnectionPool import ConnectionPool
from conftest import sqlResponse

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
    assert response.json['token'] is not None