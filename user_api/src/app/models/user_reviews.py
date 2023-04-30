import datetime
from typing import List, Optional, Any
from uuid import UUID

from pydantic import BaseModel


class UserReview(BaseModel):
    movie_id: UUID
    review_id: UUID
    user_id: Any
    created: datetime.datetime
    text: str
    like_by: Optional[List[UUID]] = []
    dislike_by: Optional[List[UUID]] = []
    rating: float = 0.0

    class Config:
        schema_extra = {
            'example': {
                'movie_id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'review_id': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                'user_id': '3fa85f64-5717-4562-b3fc-2c963f66afa4',
                'created': '2000-02-03 05:35:02',
                'text': 'text',
                'like_by': ['3fa85f64-5717-4562-b3fc-2c963f66afa6', '3fa85f74-5717-4562-b3dc-2c963k66afa7'],
                'dislike_by': ['3fa85f64-5717-4562-b3fc-2c963f66afa6', '3fa85f74-5717-4562-b3dc-2c963k66afa7'],
                'rating': 4.3,
            }
        }
