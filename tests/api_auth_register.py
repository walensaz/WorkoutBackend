from models.ConnectionPool import ConnectionPool
from conftest import sqlResponse

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
    response = client.post("/api/register", json={"firstName": "Zach", "lastName": "Wal", "password": "password"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"
    response = client.post("/api/register", json={"firstName": "Zach", "lastName": "Wal", 'email': "dc@gmail.com", "password": "Sachinfromgeekpython"})
    assert response.status_code == 200
    assert response.json['token'] is not None