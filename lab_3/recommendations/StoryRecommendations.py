
import random
from social_network.content.Feed import Feed
from social_network.content.Story import Story
from social_network.database.StoryDatabase import StoryDatabase


class StoryRecommendation(Feed):
    def __init__(self, feed_id: int | None = None):
        super().__init__(feed_id)
        self._database: StoryDatabase | None = None

    def set_database(self, database: StoryDatabase) -> None:
        """Устанавливает базу данных историй для рекомендаций."""
        if not isinstance(database, StoryDatabase):
            raise TypeError("Database must be an instance of StoryDatabase")
        self._database = database

    def add_content(self, item: Story) -> None:

        if not isinstance(item, Story):
            raise TypeError("StoryRecommendation accepts only Story instances")
        # Дополнительно: не добавлять истёкшие истории
        if item.is_expired():
            raise ValueError("Cannot add expired story to recommendation feed")
        super().add_content(item)

    def add_post(self, post) -> None:
        """Блокирует добавление Post."""
        raise TypeError("StoryRecommendation does not accept Posts")

    def show(self, count: int = 10) -> list[Story]:
        if self._database is not None:
            # Берём только активные истории из базы
            active_stories = self._database.get_all_active_stories()
            if not active_stories:
                return []
            k = min(count, len(active_stories))
            return random.sample(active_stories, k)
        else:
            # Используем только добавленные вручную (и неистёкшие)
            active_items = [
                item for item in self._items
                if isinstance(item, Story) and not item.is_expired()
            ]
            k = min(count, len(active_items))
            return random.sample(active_items, k) if active_items else []

    def __repr__(self) -> str:
        return f"StoryRecommendation(id={self.id}, items={len(self._items)})"