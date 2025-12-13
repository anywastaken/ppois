
from social_network.search.Search import Search
from social_network.database.MusicDatabase import MusicDatabase
from social_network.content.MusicTrack import MusicTrack


class MusicSearch(Search):

    def __init__(self, music_database: MusicDatabase):
        if not isinstance(music_database, MusicDatabase):
            raise TypeError("music_database must be an instance of MusicDatabase")
        self._db = music_database

    def search(self, query: str, limit: int = 10) -> list[MusicTrack]:
        normalized_query = self._validate_query(query)
        results = []

        # 1. Поиск по названию трека
        for track in self._db.get_all():
            if normalized_query in track.title.lower():
                results.append(track)

        # 2. Поиск по исполнителю
        for track in self._db.get_all():
            if track in results:
                continue
            if normalized_query in track.artist.lower():
                results.append(track)

        # 3. Поиск по жанру (точное совпадение)
        for track in self._db.get_all():
            if track in results:
                continue
            if track.genre and normalized_query == track.genre.lower():
                results.append(track)

        # Убираем дубликаты и ограничиваем лимит
        unique_results = []
        seen_ids = set()
        for track in results:
            if track.id not in seen_ids:
                unique_results.append(track)
                seen_ids.add(track.id)
                if len(unique_results) >= limit:
                    break

        return unique_results

    def search_by_id(self, track_id: int) -> MusicTrack | None:
        """
        Ищет трек по ID.
        """
        if track_id <= 0:
            return None
        return self._db.get_by_id(track_id)