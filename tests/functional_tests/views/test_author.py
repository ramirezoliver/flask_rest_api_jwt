from base64 import b64encode

import pytest


@pytest.fixture
def valid_token_header(client, empty_db):
    client.post('/register',
                json={
                    "name": "test_name",
                    "password": "test_pw",
                    })

    response = client.get('/login',
        headers={"Authorization": "Basic {}".format(b64encode(b"test_name:test_pw").decode("utf8"))}
    )

    headers = {"x-access-tokens": response.json['token']}
    return headers


def tests_create_author(client, empty_db, valid_token_header):
    data = {"name": "J.K. Rowling", "book": "Harry Potter", "country": "U.K."}
    response = client.post('/author',
        headers=valid_token_header,
        json=data)
    assert response.status_code == 201


def tests_get_authors(client, empty_db, valid_token_header):
    response = client.get('/authors', headers=valid_token_header)
    assert response.status_code == 200


def tests_delete_existing_author(client, empty_db, valid_token_header):
    data = {"name": "J.K. Rowling", "book": "Harry Potter", "country": "U.K."}
    response = client.post('/author',
        headers=valid_token_header,
        json=data)
    existing_author_id = '1'
    response = client.delete('/author/' + existing_author_id,
        headers=valid_token_header)
    assert response.status_code == 202


def tests_delete_failed(client, empty_db, valid_token_header):
    missing_author_id = '99'
    response = client.delete('/author/' + missing_author_id,
        headers=valid_token_header)
    assert response.status_code == 404
