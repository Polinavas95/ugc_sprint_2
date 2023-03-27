from config.backoff import logger
from typing import Any
from collections import defaultdict

from models.models import EventForUGS


def transform(data: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    try:
        payload = EventForUGS(**data).dict()
        payload = payload | payload["event_view"]
        event_type = payload["event_type"]
        for key in (
            "event_view",
            "event_type",
        ):
            payload.pop(key)
        return event_type, payload or {}
    except Exception as transform_ex:
        logger.exception(msg="Error while transforming data", exc_info=transform_ex)
        return data["event_type"], dict()


def order_batches(data: list[tuple[str, dict[str, Any]]]) -> dict[str, list[Any]]:
    organized_batches: dict[str, list[Any]] = defaultdict(list)
    for item in data:
        event_type, batch_item = item
        organized_batches[event_type].append(batch_item)
    return organized_batches
