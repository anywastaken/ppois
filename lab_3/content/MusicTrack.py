
from datetime import datetime


class MusicTrack:
    def __init__(self, track_id: int, title: str, artist: str, duration_seconds: int):
        if track_id <= 0:
            raise ValueError("Track ID must be a positive integer")
        if not title or not title.strip():
            raise ValueError("Track title cannot be empty")
        if not artist or not artist.strip():
            raise ValueError("Artist name cannot be empty")
        if duration_seconds <= 0 or duration_seconds > 3600:  # до 1 часа
            raise ValueError("Duration must be between 1 and 3600 seconds")

        self.id: int = track_id
        self.title: str = title.strip()
        self.artist: str = artist.strip()
        self.duration_seconds: int = duration_seconds
        self.created_at: datetime = datetime.now()
        self.is_original_audio: bool = False
        self.genre: str | None = None
        self.use_count: int = 0

    def mark_as_original(self) -> None:
        self.is_original_audio = True
        print(f"🎧 '{self.title}' помечен как оригинальный звук")

    def set_genre(self, genre: str) -> None:
        if not genre or not genre.strip():
            raise ValueError("Genre cannot be empty")
        self.genre = genre.strip()
        print(f"🎼 Жанр установлен: {self.genre}")

    def increment_use_count(self) -> None:
        self.use_count += 1

    def get_duration_formatted(self) -> str:
        mins = self.duration_seconds // 60
        secs = self.duration_seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def play(self) -> None:
        print(f"▶️ Воспроизводится: '{self.title}' — {self.artist} ({self.get_duration_formatted()})")

    def add_to_favorites(self, user_id: int) -> None:
        print(f"❤️ Трек '{self.title}' добавлен в избранное пользователем {user_id}")

    def search_by_title(self, query: str) -> bool:
        return query.lower() in self.title.lower()

    def __repr__(self) -> str:
        return f"MusicTrack(id={self.id}, title='{self.title}', artist='{self.artist}')"