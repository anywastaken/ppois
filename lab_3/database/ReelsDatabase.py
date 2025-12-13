
from social_network.database.Database import Database
from social_network.content.Reels import Reels


class ReelsDatabase(Database[Reels, int]):

    def _get_id(self, entity: Reels) -> int:
        """Извлекает ID из Reels — требуется абстрактным Database."""
        return entity.id

    def get_reels_by_author(self, author_id: int) -> list[Reels]:
        """Возвращает все Reels, созданные указанным пользователем."""
        return [reels for reels in self._storage.values() if reels.author_id == author_id]

    def get_all_reels(self) -> list[Reels]:
        """Возвращает все Reels (активные и черновики)."""
        return list(self._storage.values())

    def get_published_reels(self) -> list[Reels]:
        """Возвращает только Reels с видео (опубликованные)."""
        return [reels for reels in self._storage.values() if reels.is_video]

    def get_reels_with_music(self, track_name: str) -> list[Reels]:
        """Ищет Reels по названию музыкального трека."""
        track_lower = track_name.lower()
        return [
            reels for reels in self._storage.values()
            if reels.music_track and track_lower in reels.music_track.lower()
        ]

    def get_reels_by_location(self, location: str) -> list[Reels]:
        """Ищет Reels по местоположению."""
        loc_lower = location.lower()
        return [
            reels for reels in self._storage.values()
            if reels.location and loc_lower in reels.location.lower()
        ]

    def get_recent_reels(self, limit: int = 20) -> list[Reels]:
        """
        Возвращает последние N Reels (новые сверху).
        """
        all_reels = self.get_published_reels()
        all_reels.sort(key=lambda r: r.created_at, reverse=True)
        return all_reels[:limit]

    def count_reels_by_author(self, author_id: int) -> int:
        """Считает количество Reels у пользователя."""
        return sum(1 for reels in self._storage.values() if reels.author_id == author_id)

    def count_total_published_reels(self) -> int:
        """Считает общее количество опубликованных Reels."""
        return len(self.get_published_reels())

    def delete_reels_by_author(self, author_id: int) -> int:
        """
        Удаляет все Reels пользователя.
        Возвращает количество удалённых Reels.
        """
        to_delete = [reels.id for reels in self._storage.values() if reels.author_id == author_id]
        for reels_id in to_delete:
            del self._storage[reels_id]
        return len(to_delete)