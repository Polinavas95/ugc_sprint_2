import os
from functools import lru_cache
from pathlib import Path

from pydantic import BaseSettings, Field


class BaseConfig(BaseSettings):
    click_host: str = Field('clickhouse://localhost', env='CH_HOST')
    service_url: str = Field('http://nginx_ugc:80', env='UGC_SERVICE_URL')

    click_db: str = Field('movies', env='CH_DB')
    click_table: list[str] = Field(['movie_watch_history'])

    secret_key: str = Field(
        'ddfsfdsjlzfjdsl8fdsfhjdks7sdnaaf32jfkldsJ', env='APP_KEY'
    )
    algorithm: str = Field('HS256', env='ALGORITHM')

    # kafka_topic_name: list[str] = Field(['user_movie'], env='KAFKA_TOPIC_NAME')
    kafka_broker: str = Field('localhost:29092', env='KAFKA_BROKER')

    user: str = '6c162475-c7ed-4461-9184-001ef3d9f264'
    user2: str = '8f092fcd-1744-464f-a783-d9a6c4ec59d5'
    user3: str = '96dcc8f1-0b5e-4ed1-864f-264b9449acd2'
    movie1: str = 'a5a8f573-3cee-4ccc-8a2b-91cb9f55250a'
    movie2: str = '26e83050-29ef-4163-a99d-b546cac208f8'
    rating1: int = 4
    rating2: int = 5

    class Config:
        env_file = os.path.join(Path(__file__).parent.absolute(), '.env')
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> BaseConfig:
    return BaseConfig()
