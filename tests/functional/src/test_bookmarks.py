import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from http import HTTPStatus
from uuid import UUID
from os import path
import sys

sys.path.append(path.abspath('../..'))
from user_api.src.app.api.v1.bookmarks import router


@pytest.fixture(scope='module')
def test_app():
    app = FastAPI()
    app.include_router(router, prefix='/api/v1/bookmarks')
    yield TestClient(app)


def test_get_bookmarks(test_app):
    response = test_app.get(
        '/api/v1/bookmarks', headers={'Authorization': 'Bearer valid_token'}
    )
    assert response.status_code == HTTPStatus.OK
    assert 'bookmarks' in response.json()


def test_add_bookmarks(test_app):
    movie_id = UUID('00000000-0000-0000-0000-000000000001')
    response = test_app.post(
        f'/api/v1/bookmarks/{movie_id}',
        headers={'Authorization': 'Bearer valid_token'},
    )
    assert response.status_code == HTTPStatus.OK
    assert 'bookmarks' in response.json()


def test_delete_bookmarks(test_app):
    movie_id = UUID('00000000-0000-0000-0000-000000000001')
    response = test_app.delete(
        f'/api/v1/bookmarks/{movie_id}',
        headers={'Authorization': 'Bearer valid_token'},
    )
    assert response.status_code == HTTPStatus.OK
    assert 'bookmarks' in response.json()
