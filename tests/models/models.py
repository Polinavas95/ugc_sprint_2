from datetime import datetime

from pydantic import BaseModel, Field

from tests.factories.methods import get_new_id, get_random_num


class EventView(BaseModel):
    id: str = Field(title='uuid', default_factory=get_new_id)
    movie_id: str = Field(title='Movie id', default_factory=get_new_id)
    user_id: str = Field(title='User id', default_factory=get_new_id)
    event: str = Field(title='User id', default='')
    viewed_frame: int = Field(title='Film viewed frame', default_factory=get_random_num)
    date: int = Field(title='Date', default=datetime.now())
