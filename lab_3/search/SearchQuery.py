from social_network.search.Search import Search
from social_network.exceptions.SearchQueryException import SearchQueryException


class SearchQuery:

    # Типы поиска
    SEARCH_TYPES = {
        "users",
        "posts",
        "music",
        "reels",
        "stories",
        "subscriptions",
        "friends"
    }

    def __init__(
        self,
        user_search: Search | None = None,
        post_search: Search | None = None,
        music_search: Search | None = None,
        reels_search: Search | None = None,
        story_search: Search | None = None,
        subscription_search: Search | None = None,
        friend_search: Search | None = None
    ):
        self._search_engines = {
            "users": user_search,
            "posts": post_search,
            "music": music_search,
            "reels": reels_search,
            "stories": story_search,
            "subscriptions": subscription_search,
            "friends": friend_search
        }

    def search(
        self,
        query: str,
        limit_per_type: int = 10,
        enabled_types: list[str] | None = None
    ) -> dict[str, list]:

        if enabled_types is None:
            enabled_types = list(self.SEARCH_TYPES)
        else:
            # Проверяем корректность типов
            invalid = set(enabled_types) - self.SEARCH_TYPES
            if invalid:
                raise ValueError(f"Invalid search types: {invalid}")
            enabled_types = [t for t in self.SEARCH_TYPES if t in enabled_types]

        results = {}

        for search_type in enabled_types:
            engine = self._search_engines[search_type]
            if engine is None:
                results[search_type] = []
                continue

            try:
                found = engine.search(query, limit=limit_per_type)
                results[search_type] = found
            except Exception as e:
                # Преобразуем любую ошибку в наше персональное исключение
                raise SearchQueryException(
                    f"Search query failed for type '{search_type}': {str(e)}"
                ) from e

        return results

    def search_all(self, query: str, limit_per_type: int = 10) -> dict[str, list]:
        """Выполняет поиск по всем доступным типам."""
        return self.search(query, limit_per_type, enabled_types=None)

    def is_search_enabled(self, search_type: str) -> bool:
        """Проверяет, доступен ли поиск для указанного типа."""
        if search_type not in self.SEARCH_TYPES:
            return False
        return self._search_engines[search_type] is not None

    def get_enabled_types(self) -> list[str]:
        """Возвращает список типов, для которых подключены поисковые движки."""
        return [t for t in self.SEARCH_TYPES if self._search_engines[t] is not None]