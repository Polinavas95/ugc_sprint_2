import pytest

import clickhouse_connect

from tests.functional.settings import get_settings


@pytest.fixture(scope='session')
def clickhouse_client():
    client = clickhouse_connect.get_client(
        host=get_settings().click_host, username='default'
    )
    yield client
    client.close()
