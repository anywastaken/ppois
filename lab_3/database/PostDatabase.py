
from typing import List
from social_network.database.Database import Database
from social_network.content.Post import Post


class PostDatabase(Database[Post, int]):

    def _get_id(self, entity: Post) -> int:
        """Извлекает ID из поста — требуется абстрактным Database."""
        return entity.id

    def get_posts_by_author(self, author_id: int) -> List[Post]:
        """Возвращает все посты, созданные указанным пользователем."""
        return [post for post in self._storage.values() if post.author_id == author_id]

    def get_public_posts(self) -> List[Post]:
        """Возвращает только публичные посты."""
        return [post for post in self._storage.values() if post.is_public]

    def get_posts_with_hashtag(self, hashtag_text: str) -> List[Post]:
        """
        Ищет посты, содержащие хэштег (регистронезависимо).
        hashtag_text может быть с '#' или без.
        """
        clean_tag = hashtag_text.lstrip('#').lower()
        result = []
        for post in self._storage.values():
            for hashtag in post.hashtags:
                if hashtag.tag == clean_tag:
                    result.append(post)
                    break
        return result

    def get_recent_posts(self, limit: int = 10) -> List[Post]:
        """Возвращает последние N постов (сортировка по времени создания)."""
        # Сортируем по created_at в обратном порядке (новые сверху)
        sorted_posts = sorted(
            self._storage.values(),
            key=lambda p: p.created_at,
            reverse=True
        )
        return sorted_posts[:limit]

    def count_posts_by_author(self, author_id: int) -> int:
        """Считает количество постов пользователя."""
        return sum(1 for post in self._storage.values() if post.author_id == author_id)

    def delete_post(self, post_id: int) -> bool:
        """
        Удаляет пост из базы данных.
        Возвращает True, если пост существовал и был удалён.
        """
        if post_id in self._storage:
            del self._storage[post_id]
            return True
        return False