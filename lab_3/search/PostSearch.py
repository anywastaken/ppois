
from social_network.search.Search import Search
from social_network.database.PostDatabase import PostDatabase
from social_network.content.Post import Post


class PostSearch(Search):
    def __init__(self, post_database: PostDatabase):
        if not isinstance(post_database, PostDatabase):
            raise TypeError("post_database must be an instance of PostDatabase")
        self._db = post_database

    def search(self, query: str, limit: int = 10) -> list[Post]:

        normalized_query = self._validate_query(query)
        results = []

        # 1. Поиск по содержимому поста
        for post in self._db.get_all():
            if normalized_query in post.content.lower():
                results.append(post)

        # 2. Поиск по хэштегам
        for post in self._db.get_all():
            if post in results:
                continue
            for hashtag in post.hashtags:
                if normalized_query == hashtag.tag:  # точное совпадение
                    results.append(post)
                    break

        # 3. Поиск по ID автора (если запрос — число)
        if normalized_query.isdigit():
            author_id = int(normalized_query)
            author_posts = self._db.get_posts_by_author(author_id)
            for post in author_posts:
                if post not in results:
                    results.append(post)

        # Убираем дубликаты и ограничиваем лимит
        unique_results = []
        seen_ids = set()
        for post in results:
            if post.id not in seen_ids:
                unique_results.append(post)
                seen_ids.add(post.id)
                if len(unique_results) >= limit:
                    break

        return unique_results

    def search_by_id(self, post_id: int) -> Post | None:
        """
        Ищет пост по ID.
        """
        if post_id <= 0:
            return None
        return self._db.get_by_id(post_id)