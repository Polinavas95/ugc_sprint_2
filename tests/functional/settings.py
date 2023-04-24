import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    click_host: str = Field('clickhouse://localhost', env='CH_HOST')
    service_url: str = Field('http://localhost:8123', env='UGC_SERVICE_URL')

    click_db: str = Field('movies', env='CH_DB')
    click_table: list[str] = Field(['movie_watch_history'], env=list('EVENT_TYPES'))

    secret_key: str = Field('ddfsfdsjlzfjdsl8fdsfhjdks7sdnaaf32jfkldsJ', env='APP_KEY')
    algorithm: str = Field('HS256', env='ALGORITHM')

    kafka_topic_name: list[str] = Field(['user_movie'], env=list('EVENT_TYPES'))
    kafka_broker: str = Field('localhost:29092', env='KAFKA_BROKER')

    class Config:
        env_file = os.path.join(Path(__file__).parent.absolute(), '.env')
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> BaseConfig:
    return BaseConfig()
