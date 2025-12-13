
from social_network.content.ContentItem import ContentItem
from social_network.content.Feed import Feed
from social_network.content.MusicTrack import MusicTrack

class Reels(ContentItem):
    def __init__(self, reels_id: int, author_id: int):
        super().__init__(reels_id, author_id)
        self.is_video: bool = False
        self.caption: str | None = None
        self.music_track: MusicTrack | None = None
        self.has_effects: bool = False
        self.has_speed_control: bool = False
        self.location: str | None = None
        self.allow_comments: bool = True
        self.allow_duet: bool = True

    def record_video(self) -> None:
        """Снимает видео в реальном времени."""
        self.is_video = True
        print("🎥 Видео для Reels записано!")

    def upload_video(self) -> None:
        """Загружает видео из галереи."""
        self.is_video = True
        print("📂 Видео для Reels загружено!")

    def add_caption(self, text: str) -> None:
        """Добавляет подпись."""
        if not text or not text.strip():
            raise ValueError("Caption cannot be empty")
        self.caption = text.strip()
        print(f'💬 Подпись добавлена: "{self.caption}"')

    def add_music(self, track: MusicTrack) -> None:
        """Добавляет музыкальный трек к Reels."""
        self.music_track = f"{track.artist} — {track.title}"
        track.increment_use_count()  # обновляет счётчик использования
        print(f"🎵 Музыка добавлена: {self.music_track}")

    def apply_effects(self) -> None:
        """Применяет визуальные эффекты."""
        self.has_effects = True
        print("✨ Эффекты применены!")

    def set_speed(self, speed: float) -> None:
        """Устанавливает скорость воспроизведения (условно)."""
        if speed <= 0:
            raise ValueError("Speed must be positive")
        self.has_speed_control = True
        print(f"⏩ Скорость установлена: {speed}x")

    def add_location(self, place: str) -> None:
        """Добавляет геолокацию."""
        self.location = place.strip()
        print(f"📍 Местоположение добавлено: {self.location}")

    def disable_comments(self) -> None:
        """Отключает комментарии."""
        self.allow_comments = False
        print("🔕 Комментарии отключены")

    def disable_duet(self) -> None:
        """Отключает дуэты/ремиксы."""
        self.allow_duet = False
        print("🚫 Дуэты отключены")

    def publish_to_feed(self, feed: Feed) -> None:
        if not self.is_video:
            raise ValueError("Cannot publish Reels without video")
        if not isinstance(feed, Feed):
            raise TypeError("Feed must be an instance of Feed")
        feed.add_content(self)
        print("✅ Reels опубликовано в ленту!")



    def __repr__(self) -> str:
        status = "видео" if self.is_video else "черновик"
        return f"Reels(id={self.id}, автор={self.author_id}, статус={status})"