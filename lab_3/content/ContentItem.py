
from abc import ABC
from datetime import datetime


class ContentItem(ABC):
    def __init__(self, item_id: int, author_id: int):
        if item_id <= 0 or author_id <= 0:
            raise ValueError("IDs must be positive integers")
        self.id: int = item_id
        self.author_id: int = author_id
        self.created_at: datetime = datetime.now()

    def is_recent(self, hours: int = 24) -> bool:
        """Проверяет, создан ли контент за последние N часов."""
        from datetime import datetime, timedelta
        return datetime.now() - self.created_at < timedelta(hours=hours)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, author_id={self.author_id})"