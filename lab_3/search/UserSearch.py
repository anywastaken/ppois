
from social_network.search.Search import Search
from social_network.database.UserDatabase import UserDatabase
from social_network.user.User import User


class UserSearch(Search):
    def __init__(self, user_database: UserDatabase):
        if not isinstance(user_database, UserDatabase):
            raise TypeError("user_database must be an instance of UserDatabase")
        self._db = user_database

    def search(self, query: str, limit: int = 10) -> list[User]:
        normalized_query = self._validate_query(query)
        results = []

        # 1. Точные совпадения по username
        exact_user = self._db.get_by_username(normalized_query)
        if exact_user:
            results.append(exact_user)

        # 2. Частичные совпадения в username
        for user in self._db.get_all():
            if user is not exact_user:  # избегаем дубликата
                if normalized_query in user.username.lower():
                    results.append(user)

        # 3. Поиск в display_name и bio (через профиль)
        for user in self._db.get_all():
            if user in results:
                continue  # уже добавлен
            profile = user.profile
            name_match = (
                profile.display_name and
                normalized_query in profile.display_name.lower()
            )
            bio_match = (
                profile.bio and
                normalized_query in profile.bio.lower()
            )
            if name_match or bio_match:
                results.append(user)

        # Убираем дубликаты и ограничиваем лимит
        unique_results = []
        seen_ids = set()
        for user in results:
            if user.id not in seen_ids:
                unique_results.append(user)
                seen_ids.add(user.id)
                if len(unique_results) >= limit:
                    break

        return unique_results

    def search_by_id(self, user_id: int) -> User | None:
        if user_id <= 0:
            return None
        return self._db.get_by_id(user_id)