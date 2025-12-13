
from social_network.search.Search import Search
from social_network.subscription.Friend import Friend
from social_network.database.FriendDatabase import FriendDatabase
from social_network.exceptions.EmptySearchQueryError import EmptySearchQueryError
from social_network.exceptions.NegativeIDError import NegativeIDError

class FriendSearch(Search):

    def __init__(self, friend_database: FriendDatabase):
        if not isinstance(friend_database, FriendDatabase):
            raise TypeError("friend_database must be an instance of FriendDatabase")
        self._db = friend_database

    def search(self, query: str, limit: int = 10) -> list[Friend]:

        query = query.strip()
        if not query:
            raise EmptySearchQueryError("Search query cannot be empty")

        if not query.isdigit():
            raise ValueError("Friend search query must be a user ID (numeric)")

        user_id = int(query)
        if user_id <= 0:
            raise NegativeIDError("User ID must be positive")

        # Получаем всех друзей пользователя
        friends = []
        for friend in self._db.get_all():
            if friend.contains_user(user_id):
                friends.append(friend)

        return friends[:limit]

    def search_by_id(self, friend_id: int) -> Friend | None:
        """
        Ищет дружбу по ID.
        Но так как у Friend нет простого ID (используется составной ключ),
        этот метод не применим напрямую.
        Возвращаем None.
        """
        # Примечание: Friend использует составной ключ (user_a, user_b),
        # поэтому поиск по одному int не имеет смысла.
        return None