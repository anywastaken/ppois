from social_network.search.Search import Search
from social_network.database.StoryDatabase import StoryDatabase
from social_network.content.Story import Story


class StorySearch(Search):
    def __init__(self, story_database: StoryDatabase):
        if not isinstance(story_database, StoryDatabase):
            raise TypeError("story_database must be an instance of StoryDatabase")
        self._db = story_database

    def search(self, query: str, limit: int = 10) -> list[Story]:
        normalized_query = self._validate_query(query)
        results = []

        # Получаем только активные истории
        active_stories = self._db.get_all_active_stories()

        # 1. Поиск по подписи (caption)
        for story in active_stories:
            if story.caption and normalized_query in story.caption.lower():
                results.append(story)

        # 2. Поиск по местоположению (location)
        for story in active_stories:
            if story in results:
                continue
            if story.location and normalized_query in story.location.lower():
                results.append(story)

        # 3. Поиск по ID автора (если запрос — число)
        if normalized_query.isdigit():
            author_id = int(normalized_query)
            for story in active_stories:
                if story.author_id == author_id and story not in results:
                    results.append(story)

        # Убираем дубликаты и ограничиваем лимит
        unique_results = []
        seen_ids = set()
        for story in results:
            if story.id not in seen_ids:
                unique_results.append(story)
                seen_ids.add(story.id)
                if len(unique_results) >= limit:
                    break

        return unique_results

    def search_by_id(self, story_id: int) -> Story | None:
        """
        Ищет историю по ID (возвращает даже истёкшую).
        """
        if story_id <= 0:
            return None
        return self._db.get_by_id(story_id)

    def search_expired_by_author(self, author_id: int) -> list[Story]:
        """
        Возвращает все ИСТЁКШИЕ истории указанного автора.
        (Дополнительный удобный метод)
        """
        if author_id <= 0:
            return []
        all_expired = self._db.get_expired_stories()
        return [story for story in all_expired if story.author_id == author_id]