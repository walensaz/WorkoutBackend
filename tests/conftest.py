import os
import pytest
import sqlparse

from app import create_app
from models.ConnectionPool import Singleton


# https://flask.palletsprojects.com/en/3.0.x/testing/
# https://www.youtube.com/watch?v=RLKW7ZMJOf4

# Use autouse=True to automatically apply this fixture to each test
# Prevent interferience between tests by resetting the singleton after each test
@pytest.fixture(autouse=True)  
def reset_singleton():
    Singleton.reset_instances()
    yield
    

@pytest.fixture(scope="function")
def app():
    os.environ['USER'] = 'Test'
    os.environ['PASSWORD'] = 'Test'
    os.environ['HOST'] = 'Test'
    os.environ['PORT'] = '1234'
    os.environ['JWT_SECRET_KEY'] = '9AAC1E1BCA478D4B37C6C291E7796'
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # app.app_context()

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

def sqlResponse(rows, message):
    return {'rows': rows, 'message': message}


def test_parse():
    query = "SELECT * FROM user WHERE email = 'zwalensa@uwm.edu'"
    parsed = parse(query)
    print(parsed)

def execute_side_effects(*args, **kwargs):
    query: str = args[0]
    query_data = parse(query)
    if query_data:
        table = query_data['table']
        if query_data['query_type'] == 'SELECT':
            data_to_grab = query_data['data']
            # Lookup data if it exists, otherwise return sql error
        else:
            # It's an update, figure out what kind of update and change the memory cache as needed.
            data_to_update = query_data['data']  # Non parsed data


def parse(query, current_token=0, state={"table": "", "query_type": "", "data": "", "bool_expression": ""}):
    # Split the query into tokens
    tokens = sqlparse.parse(query)[0].tokens

    # Recursive base case: if we've processed all tokens, return the result
    if current_token == len(tokens):
        return state
    print(tokens)

    token_value = str(tokens[current_token]).upper()


    # Recursive case: process the current token and move to the next one
    if token_value in ["SELECT", "UPDATE", "INSERT INTO", "DELETE FROM"]:
        state["query_type"] = token_value
    elif token_value == "FROM" or token_value == "INTO" or (state["query_type"] == "UPDATE" and state["table"] == ""):
        state["table"] = str(tokens[current_token + 2])
    elif state["query_type"] == "INSERT INTO" and token_value == "VALUES":
        state["data"] = str(tokens[current_token + 2])
    elif state["query_type"] == "UPDATE" and token_value == "SET":
        state["data"] = str(tokens[current_token + 2])
    if "WHERE" in token_value:
        state["bool_expression"] = str(tokens[current_token])

    if token_value == "SELECT":
        state["data"] = str(tokens[current_token + 2])

    return parse(query, current_token + 1, state)

