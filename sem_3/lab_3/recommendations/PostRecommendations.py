import random
from social_network.content.Feed import Feed
from social_network.content.Post import Post
from social_network.database.PostDatabase import PostDatabase


class PostRecommendation(Feed):

    def __init__(self, feed_id: int | None = None):
        super().__init__(feed_id)
        self._database: PostDatabase | None = None

    def set_database(self, database: PostDatabase) -> None:
        """Устанавливает базу данных постов для рекомендаций."""
        if not isinstance(database, PostDatabase):
            raise TypeError("Database must be an instance of PostDatabase")
        self._database = database

    def add_content(self, item: Post) -> None:
        """
        Добавляет только Post. Отклоняет другие типы контента.
        """
        if not isinstance(item, Post):
            raise TypeError("PostRecommendation accepts only Post instances")
        # Опционально: можно фильтровать по is_public
        if not item.is_public:
            raise ValueError("Cannot add private post to recommendation feed")
        super().add_content(item)

    def add_post(self, post: Post) -> None:
        """Алиас для обратной совместимости — делегирует add_content."""
        self.add_content(post)

    def show(self, count: int = 10) -> list[Post]:
        if self._database is not None:
            # Получаем только публичные посты
            public_posts = self._database.get_public_posts()
            if not public_posts:
                return []
            k = min(count, len(public_posts))
            return random.sample(public_posts, k)
        else:
            # Используем только добавленные вручную (и публичные)
            public_items = [
                item for item in self._items
                if isinstance(item, Post) and item.is_public
            ]
            k = min(count, len(public_items))
            return random.sample(public_items, k) if public_items else []

    def __repr__(self) -> str:
        return f"PostRecommendation(id={self.id}, items={len(self._items)})"