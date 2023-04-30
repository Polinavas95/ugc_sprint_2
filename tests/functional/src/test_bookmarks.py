from http import HTTPStatus
import pytest
import requests
from uuid import uuid4

BASE_URL = 'http://localhost:8011'

token = 'my_bearer_token'
headers = {
    'Authorization': 'Bearer mock_bearer_token',
    'Content-Type': 'application/json',
}


@pytest.fixture(scope='module')
def mock_bookmark_id():
    return str(uuid4())


# Test GET /api/v1/bookmarks
def test_get_bookmarks(mock_bookmark_id):
    response = requests.get(f'{BASE_URL}/api/v1/bookmarks', headers=headers)
    print(f'{BASE_URL}/api/v1/bookmarks')
    print(requests.get(f'{BASE_URL}/api/v1/bookmarks'))
    assert response.status_code == HTTPStatus.OK
    assert 'bookmarks' in response.json()
    assert isinstance(response.json()['bookmarks'], list)


# Test POST /api/v1/bookmarks/{movie_id}
def test_add_bookmarks(mock_bookmark_id):
    print(requests.get(f'{BASE_URL}/api/v1/bookmarks', headers=headers).json())
    response = requests.post(
        f'{BASE_URL}/api/v1/bookmarks/{mock_bookmark_id}', headers=headers
    )
    print(requests.get(f'{BASE_URL}/api/v1/bookmarks', headers=headers).json())
    assert response.status_code == 200
    assert mock_bookmark_id in response.json()['bookmarks']


# Test DELETE /api/v1/bookmarks/{movie_id}
def test_delete_bookmarks(mock_bookmark_id):
    # Add a movie id to the user's bookmarks list first
    requests.post(
        f'{BASE_URL}/api/v1/bookmarks/{mock_bookmark_id}', headers=headers
    )

    response = requests.delete(
        f'{BASE_URL}/api/v1/bookmarks/{mock_bookmark_id}', headers=headers
    )
    assert response.status_code == 200
    assert mock_bookmark_id not in response.json()['bookmarks']
