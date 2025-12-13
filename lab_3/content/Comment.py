
from datetime import datetime

from social_network.content.Like import Like


class Comment:
    def __init__(
        self,
        comment_id: int,
        post_id: int,
        author_id: int,
        text: str,
        reply_to_comment_id: int | None = None
    ):
        if not text or not text.strip():
            raise ValueError("Comment text cannot be empty")
        if comment_id <= 0 or post_id <= 0 or author_id <= 0:
            raise ValueError("IDs must be positive integers")

        self.id: int = comment_id
        self.post_id: int = post_id
        self.author_id: int = author_id
        self.text: str = text.strip()
        self.reply_to_comment_id: int | None = reply_to_comment_id  # None = комментарий к посту
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime | None = None
        self.is_edited: bool = False
        self.is_deleted: bool = False

        # Ассоциации
        self.likes: list[Like] = []  # Лайки под комментарием

    def add_like(self, user_id: int) -> Like:
        """Добавляет лайк от пользователя к комментарию."""
        for like in self.likes:
            if like.user_id == user_id:
                raise ValueError("User already liked this comment")
        like_id = len(self.likes) + 1  # временно; в реальности — из БД
        like = Like(like_id=like_id, user_id=user_id, comment_id=self.id)
        self.likes.append(like)
        return like

    def remove_like(self, user_id: int) -> bool:
        """Убирает лайк пользователя."""
        for i, like in enumerate(self.likes):
            if like.user_id == user_id:
                del self.likes[i]
                return True
        return False

    def is_liked_by(self, user_id: int) -> bool:
        """Проверяет, поставил ли пользователь лайк."""
        return any(like.user_id == user_id for like in self.likes)

    def edit(self, new_text: str) -> None:
        """Редактирует текст комментария."""
        if not new_text or not new_text.strip():
            raise ValueError("New comment text cannot be empty")
        self.text = new_text.strip()
        self.updated_at = datetime.now()
        self.is_edited = True

    def delete(self) -> None:
        """Помечает комментарий как удалённый (soft delete)."""
        self.text = "[УДАЛЕНО]"
        self.is_deleted = True
        self.likes.clear()

    def get_like_count(self) -> int:
        """Возвращает количество лайков."""
        return len(self.likes)

    def is_reply(self) -> bool:
        """Проверяет, является ли комментарий ответом на другой комментарий."""
        return self.reply_to_comment_id is not None

    def __repr__(self) -> str:
        preview = self.text[:30] + "..." if len(self.text) > 30 else self.text
        return f"Comment(id={self.id}, author_id={self.author_id}, text='{preview}')"