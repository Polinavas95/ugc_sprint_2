from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    host: str = Field("localhost", env="APP_HOST")
    port: int = Field(5000, env="APP_PORT")
    batch_size: int = Field(100, env="BATCH_SIZE")


class KafkaSettings(BaseSettings):
    host: list[str] = Field(["kafka:9092"], env=list("KAFKA_HOST"))
    topics: list[str] = Field(["user_movie"], env=list("EVENT_TYPES"))
    group_id: str = Field("", env="KAFKA_GROUP_ID")
    auto_commit: bool = Field(False, env="KAFKA_ENABLE_AUTO_COMMIT")


class ClickHouseSettings(BaseSettings):
    host: str = Field("clickhouse://localhost", env="CH_HOST")
    db: str = Field("movies", env="CH_DB")
    tables: list[str] = Field(["movie_watch_history"], env=list("EVENT_TYPES"))


class Settings(BaseSettings):
    app = AppSettings()  # type: ignore
    kafka_settings = KafkaSettings()  # type: ignore
    ch_settings = ClickHouseSettings()  # type: ignore


@lru_cache
def get_settings() -> Settings:
    return Settings()
