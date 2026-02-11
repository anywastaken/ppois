
from social_network.database.Database import Database
from social_network.content.MusicTrack import MusicTrack


class MusicDatabase(Database[MusicTrack, int]):

    def _get_id(self, entity: MusicTrack) -> int:
        """Извлекает ID из трека — требуется абстрактным Database."""
        return entity.id

    def get_track_by_id(self, track_id: int) -> MusicTrack | None:
        """Возвращает трек по ID или None."""
        return self.get_by_id(track_id)

    def search_tracks(self, query: str) -> list[MusicTrack]:
        """
        Ищет треки по названию или исполнителю (регистронезависимо).
        """
        query_lower = query.lower()
        return [
            track for track in self._storage.values()
            if query_lower in track.title.lower() or query_lower in track.artist.lower()
        ]

    def get_tracks_by_artist(self, artist_name: str) -> list[MusicTrack]:
        """Возвращает все треки указанного исполнителя."""
        artist_lower = artist_name.lower()
        return [
            track for track in self._storage.values()
            if track.artist.lower() == artist_lower
        ]

    def get_tracks_by_genre(self, genre: str) -> list[MusicTrack]:
        """Возвращает треки указанного жанра."""
        genre_lower = genre.lower()
        return [
            track for track in self._storage.values()
            if track.genre and track.genre.lower() == genre_lower
        ]

    def get_original_tracks(self) -> list[MusicTrack]:
        """Возвращает только оригинальные звуки (записанные пользователями)."""
        return [track for track in self._storage.values() if track.is_original_audio]

    def get_popular_tracks(self, limit: int = 10) -> list[MusicTrack]:
        """
        Возвращает самые популярные треки (по use_count), отсортированные по убыванию.
        """
        sorted_tracks = sorted(
            self._storage.values(),
            key=lambda t: t.use_count,
            reverse=True
        )
        return sorted_tracks[:limit]

    def get_recent_tracks(self, limit: int = 20) -> list[MusicTrack]:
        """
        Возвращает последние добавленные треки (новые сверху).
        """
        # Предполагаем, что порядок добавления сохраняется в dict (Python 3.7+)
        all_tracks = list(self._storage.values())
        return all_tracks[-limit:][::-1]  # последние N, в обратном порядке (новые первыми)

    def count_tracks(self) -> int:
        """Возвращает общее количество треков."""
        return len(self._storage)

    def count_tracks_by_artist(self, artist_name: str) -> int:
        """Считает количество треков исполнителя."""
        return len(self.get_tracks_by_artist(artist_name))

    def delete_track(self, track_id: int) -> bool:
        """Удаляет трек по ID."""
        return self.remove(track_id)