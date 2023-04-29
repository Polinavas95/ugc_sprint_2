from http import HTTPStatus

import requests
from uuid import uuid4

BASE_URL = 'http://localhost:8011'
mock_bookmark_id = uuid4()

token = 'my_bearer_token'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}


# Test GET /api/v1/bookmarks
def test_get_bookmarks():
    response = requests.get(f'{BASE_URL}/api/v1/bookmarks', headers=headers)
    print(f'{BASE_URL}/api/v1/bookmarks')
    print(requests.get(f'{BASE_URL}/api/v1/bookmarks'))
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'bookmarks': []
    }   # Assuming an empty bookmarks list for a new user


# Test POST /api/v1/bookmarks/{movie_id}
def test_add_bookmarks():
    response = requests.post(
        f'{BASE_URL}/api/v1/bookmarks/{mock_bookmark_id}', headers=headers
    )
    assert response.status_code == 200
    assert response.json() == {
        'bookmarks': [mock_bookmark_id]
    }   # Assuming the movie id was successfully added


# Test DELETE /api/v1/bookmarks/{movie_id}
def test_delete_bookmarks():
    # Add a movie id to the user's bookmarks list first
    requests.post(f'{BASE_URL}/api/v1/bookmarks/{mock_bookmark_id}')

    response = requests.delete(
        f'{BASE_URL}/api/v1/bookmarks/{mock_bookmark_id}'
    )
    assert response.status_code == 200
    assert response.json() == {
        'bookmarks': []
    }   # Assuming the movie id was successfully removed
