from typing import List


# Подсчет числа лайков от общего числа оценок
def get_rating(like_by: List[str], dislike_by: List[str]) -> float:
    if not like_by:
        return 0.0
    return len(like_by) * 10 / (len(like_by) + len(dislike_by))
