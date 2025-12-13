
from datetime import datetime


class Friend:
    def __init__(self, user1_id: int, user2_id: int):
        if user1_id <= 0 or user2_id <= 0:
            raise ValueError("User IDs must be positive integers")
        if user1_id == user2_id:
            raise ValueError("User cannot be friends with themselves")

        # Нормализуем порядок: всегда меньший ID первым
        if user1_id < user2_id:
            self.user_a: int = user1_id
            self.user_b: int = user2_id
        else:
            self.user_a: int = user2_id
            self.user_b: int = user1_id

        self.created_at: datetime = datetime.now()

    def contains_user(self, user_id: int) -> bool:
        """Проверяет, участвует ли пользователь в этой дружбе."""
        return user_id == self.user_a or user_id == self.user_b

    def get_other_user(self, user_id: int) -> int:
        """Возвращает ID другого пользователя."""
        if user_id == self.user_a:
            return self.user_b
        elif user_id == self.user_b:
            return self.user_a
        else:
            raise ValueError("User is not part of this friendship")

    def __eq__(self, other) -> bool:
        if isinstance(other, Friend):
            return self.user_a == other.user_a and self.user_b == other.user_b
        return False

    def __hash__(self) -> int:
        return hash((self.user_a, self.user_b))

    def __repr__(self) -> str:
        return f"Friend({self.user_a} ↔ {self.user_b})"