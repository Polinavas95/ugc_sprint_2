import asyncio
import uuid
from random import choice, randint

import jwt
import pytest
import pytest_asyncio

import clickhouse_connect
import aiohttp

from tests.functional.settings import get_settings


@pytest.fixture(scope='session')
def clickhouse_client():
    client = clickhouse_connect.get_client(
        host=get_settings().click_host, username='default'
    )
    yield client
    client.close()


@pytest_asyncio.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
def access_token():
    data = {'sub': get_settings().user, 'permissions': [], 'is_super': True}
    return jwt.encode(data, get_settings().secret_key, get_settings().algorithm)


@pytest_asyncio.fixture(scope='session')
def movie_id():
    return str(uuid.uuid4())


@pytest_asyncio.fixture(scope='session')
def event_type():
    return choice(['user_movie', ])


@pytest_asyncio.fixture(scope='session')
def event():
    return randint(1, 10000)
