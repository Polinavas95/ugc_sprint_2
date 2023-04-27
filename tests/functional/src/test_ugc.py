
from http import HTTPStatus

import pytest

from tests.functional.settings import get_settings
pytestmark = pytest.mark.asyncio


url_event = f'{get_settings().service_url}/api/v1/movies/event'


async def test_producer_unauthorized(session, event):
    """Проверка доступа неавторизованного пользователя к эндпоинту загрузки единичного события"""

    url = url_event
    params = {'event': event}

    async with session.post(url, params=params) as response:
        assert response.status == HTTPStatus.FORBIDDEN


async def test_producer_authorized(session, access_token, event):
    """Проверка выполнения загрузки единичного события авторизованного пользователя"""

    url = url_event
    params = {'event': event}
    headers = {'Authorization': 'Bearer ' + access_token}

    async with session.post(url, params=params, headers=headers) as response:
        assert response.status == HTTPStatus.OK
