from social_network.content.ContentItem import ContentItem
from social_network.content.Post import Post


class Feed:
    def __init__(self, feed_id: int | None = None):
        self.id: int | None = feed_id
        self._items: list[ContentItem] = []

    def add_content(self, item: ContentItem) -> None:
        """Добавляет любой контент в ленту."""
        if not isinstance(item, ContentItem):
            raise TypeError("Only ContentItem instances can be added to Feed")
        self._items.append(item)

    def add_post(self, post) -> None:  # для обратной совместимости
        self.add_content(post)

    def get_items(self, limit: int | None = None) -> list[ContentItem]:
        if limit is None:
            return self._items.copy()
        return self._items[:limit]

    def get_posts(self, limit: int | None = None) -> list[Post]:
        """Возвращает список только постов из ленты."""
        posts = [item for item in self._items if isinstance(item, Post)]
        if limit is not None:
            posts = posts[-limit:]  # последние N постов
        return posts

    def remove_post(self, post_id: int) -> bool:
        initial_count = len(self._items)
        self._items = [
            item for item in self._items
            if not (isinstance(item, Post) and getattr(item, 'id', None) == post_id)
        ]
        return len(self._items) < initial_count

    def get_item_count(self) -> int:
        return len(self._items)

    def clear(self) -> None:
        self._items.clear()

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __repr__(self) -> str:
        return f"Feed(id={self.id}, items={len(self._items)})"