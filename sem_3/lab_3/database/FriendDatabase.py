
from typing import List
from social_network.database.Database import Database
from social_network.subscription.Friend import Friend


class FriendDatabase(Database[Friend, tuple[int, int]]):

    def _get_id(self, entity: Friend) -> tuple[int, int]:
        return entity.user_a, entity.user_b

    def add_friendship(self, user1_id: int, user2_id: int) -> None:
        """Устанавливает дружбу между двумя пользователями."""
        friendship = Friend(user1_id, user2_id)
        self.add(friendship)

    def remove_friendship(self, user1_id: int, user2_id: int) -> bool:
        """Удаляет дружбу."""
        # Нормализуем порядок
        a, b = (user1_id, user2_id) if user1_id < user2_id else (user2_id, user1_id)
        return self.remove((a, b))

    def are_friends(self, user1_id: int, user2_id: int) -> bool:
        """Проверяет, являются ли пользователи друзьями."""
        a, b = (user1_id, user2_id) if user1_id < user2_id else (user2_id, user1_id)
        return self.exists((a, b))

    def get_friends_of(self, user_id: int) -> List[int]:
        """Возвращает список ID друзей пользователя."""
        friends = []
        for friend in self._storage.values():
            if friend.contains_user(user_id):
                friends.append(friend.get_other_user(user_id))
        return friends

    def get_friend_count(self, user_id: int) -> int:
        """Считает количество друзей у пользователя."""
        return len(self.get_friends_of(user_id))

    def get_mutual_friends(self, user1_id: int, user2_id: int) -> List[int]:
        """Возвращает список общих друзей двух пользователей."""
        friends1 = set(self.get_friends_of(user1_id))
        friends2 = set(self.get_friends_of(user2_id))
        return list(friends1 & friends2)