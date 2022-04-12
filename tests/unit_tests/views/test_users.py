from base64 import b64encode

import pytest

from library.app import create_app, db
from library.models.users import Users


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here


@pytest.fixture()
def client(app):
    yield app.test_client()


@pytest.fixture
def empty_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


USER_1 = dict(
    name='fake_name',
    password='fake_pass',
    admin=False,
)


@pytest.fixture
def database(empty_db):
    user1 = Users(**USER_1)

    db.session.add_all([user1])
    db.session.commit()


def tests_register_user(client, database):
    response = client.post('/register',
                        json={
                            "name": "test_name",
                            "password": "test_pw",
                            }
                        )
    assert response.status_code == 201


def tests_login_valid(client, database):
    client.post('/register',
                        json={
                            "name": "test_name",
                            "password": "test_pw",
                            }
    )

    response = client.get('/login',
        headers={"Authorization": "Basic {}".format(b64encode(b"test_name:test_pw").decode("utf8"))}
    )
    assert response.status_code == 200


def tests_get_users(client, database):
    response = client.post('/users')
    assert response.status_code == 200
