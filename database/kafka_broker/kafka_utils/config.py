from functools import lru_cache

from pydantic import BaseSettings, Field


class KafkaSettings(BaseSettings):
    kafka_topic_name: str = Field('user_movie', env='KAFKA_TOPIC_NAME')
    kafka_broker: str = Field('localhost:29092', env='KAFKA_BROKER')


class Settings(BaseSettings):
    kafka_settings = KafkaSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
