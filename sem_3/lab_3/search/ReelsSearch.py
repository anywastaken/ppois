
from social_network.search.Search import Search
from social_network.database.ReelsDatabase import ReelsDatabase
from social_network.content.Reels import Reels


class ReelsSearch(Search):
    def __init__(self, reels_database: ReelsDatabase):
        if not isinstance(reels_database, ReelsDatabase):
            raise TypeError("reels_database must be an instance of ReelsDatabase")
        self._db = reels_database

    def search(self, query: str, limit: int = 10) -> list[Reels]:
        normalized_query = self._validate_query(query)
        results = []

        # 1. Поиск по подписи
        for reels in self._db.get_all():
            if reels.caption and normalized_query in reels.caption.lower():
                results.append(reels)

        # 2. Поиск по музыке
        for reels in self._db.get_all():
            if reels in results:
                continue
            if reels.music_track:  # ← это гарантирует, что music_track не None
                if normalized_query in reels.music_track.title.lower():
                    results.append(reels)

        # 3. Поиск по местоположению
        for reels in self._db.get_all():
            if reels in results:
                continue
            if reels.location and normalized_query in reels.location.lower():
                results.append(reels)

        # Убираем дубликаты и ограничиваем лимит
        unique_results = []
        seen_ids = set()
        for reels in results:
            if reels.id not in seen_ids:
                unique_results.append(reels)
                seen_ids.add(reels.id)
                if len(unique_results) >= limit:
                    break

        return unique_results

    def search_by_id(self, reels_id: int) -> Reels | None:
        """
        Ищет Reels по ID.
        """
        if reels_id <= 0:
            return None
        return self._db.get_by_id(reels_id)