import random
import uuid
from datetime import datetime

from src.app.models.user_reviews import UserReview
from tests.core.string_utils import generate_random_string


def create_review() -> UserReview:
    """Создание рандомного объекта ревью.

    Returns: Review
    """
    return UserReview(
        movie_id=uuid.uuid4(),
        review_id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        created=datetime.now().isoformat(),
        text=generate_random_string(),
        like_by=[uuid.uuid4(), uuid.uuid4()],
        dislike_by=[uuid.uuid4(), uuid.uuid4()],
        rating=4.3
    )


def get_random_num() -> int:
    return random.randint(1, 1000)


def get_new_id() -> str:
    return str(uuid.uuid4())