from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBearer

from user_api.src.app.models.film_likes_schema import MovieLikeSchema
from user_api.src.app.service.auth import Auth
from user_api.src.app.service.likes import (
    MovieLikesService,
    get_user_bookmarks_service,
)

auth_handler = Auth()
router = APIRouter()
security = HTTPBearer()


@router.post(
    '/{movie_id}',
    response_model=MovieLikeSchema,
    description='Добавляет лайки/дизлайки к фильму',
    response_description='Возвращает фильм с лайками/дизлайками/рейтингом',
)
async def add_like_dislike(
    movie_id: UUID,
    like: bool,
    user_id: str = Depends(auth_handler),
    likes_service: MovieLikesService = Depends(get_user_bookmarks_service),
) -> MovieLikeSchema:
    movie_user_data = await likes_service.add_like_dislike(
        user_id, movie_id, like
    )
    return movie_user_data


@router.put(
    '/{movie_id}',
    description='Удаляет лайки или дизлайки из фильма от конкретного user',
    response_description='Возвращает фильм с рейтингом, лайками или дизлайками',
    response_model=MovieLikeSchema,
)
async def remove_like_dislike(
    movie_id: UUID,
    like: bool,
    user_id: str = Depends(auth_handler),
    likes_service: MovieLikesService = Depends(get_user_bookmarks_service),
) -> MovieLikeSchema:
    try:
        if movie_user_data := await likes_service.remove_like_dislike(
            user_id, movie_id, like
        ):
            return movie_user_data
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Movie with {movie_id} not found.',
        )
    except ValueError as e:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f'Nothing to remove. User {user_id } not found in movie assessment.',
        ) from e


@router.get(
    '/{movie_id}',
    description='Возвращает данные о фильме',
    response_description='Возвращает фильм с лайками/дизлайками/рейтингом',
    response_model=MovieLikeSchema,
)
async def get_like_dislike(
    movie_id: UUID,
    likes_service: MovieLikesService = Depends(get_user_bookmarks_service),
    credentials: HTTPBasicCredentials = Depends(security),
) -> MovieLikeSchema:
    token = credentials.credentials  # type: ignore[attr-defined]
    auth_handler.decode_token(token)

    if movie_user_data := await likes_service.get(movie_id):
        return movie_user_data
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=f'Movie with {movie_id} not found.',
    )
