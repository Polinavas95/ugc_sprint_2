from fastapi import APIRouter

from utils.kafka_producer import KafkaUserMovieProducer
from config.config import get_settings

settings = get_settings()
producer = KafkaUserMovieProducer(
    topic=settings.kafka_settings.kafka_topic_name,
    bootstrap_servers=settings.kafka_settings.kafka_broker,
)

api_router = APIRouter(
    prefix="/v1/api",
    responses={404: {"description": "Not found"}},
)


@api_router.get('/')
def read_root() -> dict[str, str]:
    return {'Hello': 'World'}


@api_router.get('/movies/event', tags=['viewed_film'])
def read_item() -> dict[str, str]:
    event = producer.send_generated_event()

    return {'msg': f'Event sent: {event}'}
