from typing import Optional, Type
from uuid import UUID

from fastapi import Depends
from motor.core import AgnosticCollection

from app.db.mongo_db import get_mongo
from app.models.user_bookmarks import UserBookmarks


class UserBookmarksService:
    def __init__(
        self, model: Type[UserBookmarks], collection: AgnosticCollection
    ):
        self.model = model
        self.collection = collection

    async def add(self, user_id: str, movie_id: UUID) -> UserBookmarks:
        document = {
            'user_id': user_id,
            'film_id': hash(str(movie_id)),
            'bookmarks': [str(movie_id)],
        }
        user_filter = {'user_id': user_id}
        # Insert a single document
        await self.collection.insert_one(document)
        # Get a single document from the database
        new_document = await self.collection.find_one(user_filter)
        return self.model(**new_document)

    async def remove(self, user_id: str, movie_id: UUID) -> UserBookmarks:
        user_filter = {'user_id': user_id, 'film_id': {'$exists': True}}
        await self.collection.update_one(
            user_filter, {'$pull': {'bookmarks': str(movie_id)}}
        )
        new_document = await self.collection.find_one(user_filter)
        return self.model(**new_document)

    async def get(self, user_id: str) -> Optional[UserBookmarks]:
        user_filter = {'user_id': user_id, 'film_id': {'$exists': True}}
        bookmarks = await self.collection.find_one(user_filter)
        if bookmarks:
            return self.model(**bookmarks)
        return None


def get_user_bookmarks_service(
    mongo: AgnosticCollection = Depends(get_mongo),
) -> UserBookmarksService:
    collection = mongo.get_collection('user_bookmarks')
    return UserBookmarksService(UserBookmarks, collection)
