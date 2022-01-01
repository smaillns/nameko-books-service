import json
import pytest


@pytest.fixture
def new_author(web_session):
    response = web_session.post('/authors', data=json.dumps({
        "name": "new author name",
        "gender": "Male"
    }))
    return response


@pytest.fixture
def new_book(web_session, new_author):
    response = web_session.post('/books', data=json.dumps({
        "author_id": new_author.json()['id'],
        "title": "book title"
    }))
    return response


def test_insert_book(web_session, create_svc, new_author, new_book):
    response = web_session.post('/books', data=json.dumps({
        "author_id": new_author.json()['id'],
        "title": "title"
    }))
    assert response.status_code == 201
    assert response.json()['id'] > 0


def test_get_book(web_session, create_svc, new_book):
    resp = web_session.get('/books/{}'.format(new_book.json()['id']))
    assert resp.status_code == 200
    assert resp.json()['id'] == new_book.json()['id']


def test_delete_book(web_session, create_svc, new_book):
    resp = web_session.delete('/books/{}'.format(new_book.json()['id']))
    assert resp.status_code == 204


def test_update_book(web_session, create_svc, new_book):
    resp = web_session.put('/books/{}'.format(new_book.json()['id']), data=json.dumps({
        "title": "updated title"
    }))
    assert resp.status_code == 200


# -------------------
# non-happy flow
# -------------------

def test_when_book_not_found(web_session, create_svc):
    response = web_session.get('/book/9999999999999')
    assert response.status_code == 404


def test_create_book_fails_with_invalid_json(web_session, create_svc):
    response = web_session.post('/books', data=json.dumps({
        "test": 1
    }))
    assert response.json()['error'] == 'BAD_REQUEST'
