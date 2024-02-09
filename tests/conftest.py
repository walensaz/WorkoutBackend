import os

import pytest

from app import create_app

# https://flask.palletsprojects.com/en/3.0.x/testing/
# https://www.youtube.com/watch?v=RLKW7ZMJOf4

@pytest.fixture()
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


@pytest.fixture()
def client(app):
    return app.test_client()

