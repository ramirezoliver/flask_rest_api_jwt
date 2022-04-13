from base64 import b64encode


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
    assert type(response.json['token']) == str


def tests_login_invalid(client, database):
    client.post('/register',
                        json={
                            "name": "test_name",
                            "password": "test_pw",
                            }
    )

    response = client.get('/login',
        headers={"Authorization": "Basic {}".format(b64encode(b"test_name:wrong_pw").decode("utf8"))}
    )
    assert response.status_code == 401


def tests_get_users(client, database):
    response = client.post('/users')
    assert response.status_code == 200
