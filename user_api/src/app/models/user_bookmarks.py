from typing import List
from uuid import UUID

from pydantic import BaseModel


class UserBookmarks(BaseModel):
    bookmarks: List[UUID]

    class Config:
        schema_extra = {
            'example': {
                'bookmarks': ['3fa85f64-5717-4562-b3fc-2c963f66afa6', '3fa85f74-5717-4562-b3dc-2c963k66afa7']
            }
        }
