from http import HTTPStatus

import requests
from uuid import uuid4

BASE_URL = "http://localhost:8011"
token = 'my_bearer_token'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
payload = {
    'movie_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
    'likes': 45,
    'dislikes': 10,
    'rating': 4.3,
}
movie_id_add = uuid4()


def test_add_like_dislike():
    url = f"{BASE_URL}/api/v1/likes/{movie_id_add}/?movie_id={movie_id_add}&like=True"

    response = requests.post(url, json=payload, headers=headers)

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "dislikes": 0,
        "likes": 1,
        "movie_id": str(movie_id_add),
        'rating': 10.0
    }


def test_remove_like_dislike():
    movie_id = uuid4()
    url = f"{BASE_URL}/api/v1/likes/{movie_id}/?movie_id={movie_id}&like=False"

    response = requests.post(url, headers=headers)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "dislikes": 1,
        "likes": 0,
        "movie_id": str(movie_id),
        'rating': 0.0
    }

    response = requests.put(url, headers=headers)
    assert response.status_code == HTTPStatus.OK
