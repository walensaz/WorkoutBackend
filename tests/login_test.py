from models.ConnectionPool import ConnectionPool
from tests.conftest import app, client, sqlResponse

def test_login(client):
    def side_effects(*args, **kwargs):
        if args[0] == 'SELECT * FROM user WHERE email = %s':
            if args[1] == ('dc@gmail.com',):
                return sqlResponse([{'email': 'dc@gmail.com', 'password_hash': '$2b$12$2z2bCyIFSuCVcT/iGt1HNOUhxw7aSpR2MlrbbINzGMyhFIT.5rm9S'}], "")
            
            elif args[1] == ('a@gmail.com',):
                return {'rows': ['a@gmail.com'], 'message': ""}
            else:
                return {'rows': [], 'message': ""}
        else:
            return {'rows': [], 'message': ""}
    ConnectionPool(testEffects=side_effects)

    response = client.post("/api/login", json={"email": "dc@gmail.com"})
    assert response.status_code == 400
    response = client.post("/api/login", json={"password": "password"})
    assert response.status_code == 400
    assert response.json['message'] == "Missing field: email"
    # wrong password
    response = client.post("/api/login", json={'email': "dc@gmail.com", "password": "password"})
    assert response.status_code == 401
    assert response.json['message'] == "Invalid credentials"
    # nonexistant email
    response = client.post("/api/login", json={'email': "abcd@gmail.com", "password": "password"})
    assert response.status_code == 401
    assert response.json['message'] == "Invalid credentials"
    response = client.post("/api/login", json={'email': "dc@gmail.com", "password": "Sachinfromgeekpython"})
    assert response.status_code == 200
    assert response.json['token'] is not None