
import random
from social_network.content.MusicTrack import MusicTrack
from social_network.database.MusicDatabase import MusicDatabase


class MusicRecommendation:
    def __init__(self, recommendation_id: int | None = None):
        self.id: int | None = recommendation_id
        self._database: MusicDatabase | None = None
        self._custom_tracks: list[MusicTrack] = []

    def set_database(self, database: MusicDatabase) -> None:
        """Устанавливает базу данных треков."""
        if not isinstance(database, MusicDatabase):
            raise TypeError("Database must be an instance of MusicDatabase")
        self._database = database

    def add_track(self, track: MusicTrack) -> None:
        """Добавляет трек вручную (для кастомных рекомендаций)."""
        if not isinstance(track, MusicTrack):
            raise TypeError("Only MusicTrack instances are allowed")
        if track not in self._custom_tracks:
            self._custom_tracks.append(track)

    def show(self, count: int = 10, strategy: str = "popular") -> list[MusicTrack]:
        if self._database is not None:
            if strategy == "popular":
                tracks = self._database.get_popular_tracks(limit=count * 2)
            elif strategy == "recent":
                tracks = self._database.get_recent_tracks(limit=count * 2)
            elif strategy == "random":
                all_tracks = list(self._database._storage.values())
                if len(all_tracks) <= count:
                    tracks = all_tracks
                else:
                    tracks = random.sample(all_tracks, count * 2)
            else:
                tracks = self._database.get_popular_tracks(limit=count * 2)
        else:
            # Используем только кастомные треки
            tracks = self._custom_tracks.copy()

        # Убираем дубликаты и обрезаем до count
        seen_ids = set()
        unique_tracks = []
        for track in tracks:
            if track.id not in seen_ids:
                unique_tracks.append(track)
                seen_ids.add(track.id)
                if len(unique_tracks) >= count:
                    break

        # Если не хватает — добавляем из кастомных
        if len(unique_tracks) < count:
            for track in self._custom_tracks:
                if track.id not in seen_ids:
                    unique_tracks.append(track)
                    seen_ids.add(track.id)
                    if len(unique_tracks) >= count:
                        break

        return unique_tracks[:count]

    def get_total_available(self) -> int:
        """Возвращает общее количество доступных треков для рекомендаций."""
        if self._database:
            return len(self._database._storage) + len(self._custom_tracks)
        return len(self._custom_tracks)

    def __repr__(self) -> str:
        total = self.get_total_available()
        return f"MusicRecommendation(id={self.id}, available_tracks={total})"