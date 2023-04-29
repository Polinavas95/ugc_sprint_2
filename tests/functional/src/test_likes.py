import requests
from uuid import uuid4

BASE_URL = "http://localhost:8000"


def test_add_like_dislike():
    movie_id = uuid4()
    url = f"{BASE_URL}/api_ugc/{movie_id}"
    payload = {"like": True}
    headers = {"Authorization": "Bearer <token>"}

    response = requests.post(url, json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == {
        "movie_id": str(movie_id),
        "like_count": 1,
        "dislike_count": 0,
    }


def test_remove_like_dislike():
    movie_id = uuid4()
    url = f"{BASE_URL}/api_ugc/{movie_id}"
    payload = {"like": True}
    headers = {"Authorization": "Bearer <token>"}

    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200

    response = requests.put(url, json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "movie_id": str(movie_id),
        "like_count": 0,
        "dislike_count": 0,
    }


def test_get_like_dislike():
    movie_id = uuid4()
    url = f"{BASE_URL}/api_ugc/{movie_id}"
    payload = {"like": True}
    headers = {"Authorization": "Bearer <token>"}

    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 200

    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "movie_id": str(movie_id),
        "like_count": 1,
        "dislike_count": 0,
    }
