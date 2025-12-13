
from social_network.database.Database import Database
from social_network.content.Story import Story


class StoryDatabase(Database[Story, int]):
    def _get_id(self, entity: Story) -> int:
        """Извлекает ID из истории — требуется абстрактным Database."""
        return entity.id

    def get_stories_by_author(self, author_id: int) -> list[Story]:
        """Возвращает все истории, созданные указанным пользователем."""
        return [story for story in self._storage.values() if story.author_id == author_id]

    def get_active_stories_by_author(self, author_id: int) -> list[Story]:
        """Возвращает только неистёкшие истории пользователя."""
        return [
            story for story in self._storage.values()
            if story.author_id == author_id and not story.is_expired()
        ]

    def get_all_active_stories(self) -> list[Story]:
        """Возвращает все неистёкшие истории во всей системе."""
        return [story for story in self._storage.values() if not story.is_expired()]

    def get_expired_stories(self) -> list[Story]:
        """Возвращает все истёкшие истории (для очистки)."""
        return [story for story in self._storage.values() if story.is_expired()]

    def count_active_stories(self) -> int:
        """Считает количество активных (неистёкших) историй."""
        return sum(1 for story in self._storage.values() if not story.is_expired())

    def delete_expired_stories(self) -> int:
        """
        Удаляет все истёкшие истории из базы.
        Возвращает количество удалённых историй.
        """
        expired_ids = [story.id for story in self._storage.values() if story.is_expired()]
        for story_id in expired_ids:
            del self._storage[story_id]
        return len(expired_ids)

    def get_recent_stories(self, limit: int = 20) -> list[Story]:
        """
        Возвращает последние N активных историй (новые сверху).
        """
        active = self.get_all_active_stories()
        # Сортируем по времени создания (новые первыми)
        active.sort(key=lambda s: s.created_at, reverse=True)
        return active[:limit]

    def has_active_story(self, author_id: int) -> bool:
        """Проверяет, есть ли у пользователя хотя бы одна активная история."""
        return any(
            story.author_id == author_id and not story.is_expired()
            for story in self._storage.values()
        )