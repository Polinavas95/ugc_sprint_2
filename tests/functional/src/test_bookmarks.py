import requests

BASE_URL = 'http://localhost:8011'

token = 'my_bearer_token'
headers = {'Authorization': f'Bearer {token}'}

# Test GET /api/v1/bookmarks
def test_get_bookmarks():
    response = requests.get(f'{BASE_URL}/api/v1/bookmarks', headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        'bookmarks': []
    }   # Assuming an empty bookmarks list for a new user


# Test POST /api/v1/bookmarks/{movie_id}
def test_add_bookmarks():
    response = requests.post(f'{BASE_URL}/api/v1/bookmarks/some-movie-id')
    assert response.status_code == 200
    assert response.json() == {
        'bookmarks': ['some-movie-id']
    }   # Assuming the movie id was successfully added


# Test DELETE /api/v1/bookmarks/{movie_id}
def test_delete_bookmarks():
    # Add a movie id to the user's bookmarks list first
    requests.post(f'{BASE_URL}/api/v1/bookmarks/some-movie-id')

    response = requests.delete(f'{BASE_URL}/api/v1/bookmarks/some-movie-id')
    assert response.status_code == 200
    assert response.json() == {
        'bookmarks': []
    }   # Assuming the movie id was successfully removed
