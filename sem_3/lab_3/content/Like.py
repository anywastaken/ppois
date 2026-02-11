
from datetime import datetime


class Like:
    def __init__(
        self,
        like_id: int,
        user_id: int,
        post_id: int | None = None,
        comment_id: int | None = None
    ):
        if like_id <= 0 or user_id <= 0:
            raise ValueError("IDs must be positive integers")

        if (post_id is None and comment_id is None) or \
           (post_id is not None and comment_id is not None):
            raise ValueError(
                "Like must be associated with exactly one of: post_id or comment_id"
            )

        self.id: int = like_id
        self.user_id: int = user_id
        self.post_id: int | None = post_id
        self.comment_id: int | None = comment_id
        self.created_at: datetime = datetime.now()

    def is_on_post(self) -> bool:
        """Возвращает True, если лайк поставлен под пост."""
        return self.post_id is not None

    def is_on_comment(self) -> bool:
        """Возвращает True, если лайк поставлен под комментарий."""
        return self.comment_id is not None

    def get_target_id(self) -> int:
        """Возвращает ID целевого объекта (поста или комментария)."""
        if self.post_id is not None:
            return self.post_id
        return self.comment_id  # точно не None, если не на посте

    def get_target_type(self) -> str:
        """Возвращает тип цели: 'post' или 'comment'."""
        return "post" if self.post_id is not None else "comment"

    def __repr__(self) -> str:
        target = "post" if self.post_id else "comment"
        target_id = self.post_id or self.comment_id
        return f"Like(id={self.id}, user_id={self.user_id}, on_{target}={target_id})"