from __future__ import annotations

from collections.abc import Callable
from datetime import datetime
from typing import Any
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v: Any, *, default: Callable[[Any], Any] | None) -> str:
    return orjson.dumps(v, default=default).decode()


class ConfigMixin(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class EventView(ConfigMixin):
    movie_id: UUID
    user_id: UUID
    event: str
    viewed_frame: int
    date: datetime

    def dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        result: dict[str, Any] = super().dict(*args, **kwargs)
        result['movie_id'] = str(result['movie_id'])
        result['user_id'] = str(result['user_id'])
        return result


class EventForUGS(ConfigMixin):
    event_view: EventView
    ip: str
    event_type: str
    timezone: str
