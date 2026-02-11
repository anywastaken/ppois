
import random
from social_network.content.Feed import Feed
from social_network.content.Reels import Reels
from social_network.database.ReelsDatabase import ReelsDatabase


class ReelsRecommendation(Feed):

    def __init__(self, feed_id: int | None = None):
        super().__init__(feed_id)
        self._database: ReelsDatabase | None = None

    def set_database(self, database: ReelsDatabase) -> None:
        """Устанавливает базу данных Reels для рекомендаций."""
        if not isinstance(database, ReelsDatabase):
            raise TypeError("Database must be an instance of ReelsDatabase")
        self._database = database

    def add_content(self, item: Reels) -> None:
        """
        Добавляет только Reels. Отклоняет другие типы контента.
        """
        if not isinstance(item, Reels):
            raise TypeError("ReelsRecommendation accepts only Reels instances")
        super().add_content(item)

    def add_post(self, post) -> None:
        """Блокирует добавление Post."""
        raise TypeError("ReelsRecommendation does not accept Posts")

    def show(self, count: int = 10) -> list[Reels]:
        if self._database is not None:
            # Берём случайные Reels из базы данных
            all_reels = self._database.get_published_reels()
            if not all_reels:
                return []
            # Выбираем случайные без повторений
            k = min(count, len(all_reels))
            return random.sample(all_reels, k)
        else:
            # Используем только то, что добавлено вручную
            reels_only = [item for item in self._items if isinstance(item, Reels)]
            k = min(count, len(reels_only))
            return random.sample(reels_only, k) if reels_only else []

    def __repr__(self) -> str:
        return f"ReelsRecommendation(id={self.id}, items={len(self._items)})"