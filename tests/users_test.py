from models.ConnectionPool import ConnectionPool
from tests.conftest import app, client, sqlResponse

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