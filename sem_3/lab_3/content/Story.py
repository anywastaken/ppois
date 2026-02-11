from datetime import datetime, timedelta
from social_network.content.ContentItem import ContentItem
from social_network.content.Feed import Feed


class Story(ContentItem):
    def __init__(self, story_id: int, author_id: int):
        super().__init__(story_id, author_id)
        self.is_video: bool = False
        self.caption: str | None = None
        self.expires_at: datetime = self.created_at + timedelta(hours=24)
        self.has_sticker: bool = False
        self.filter_applied: str | None = None
        self.location: str | None = None

    def record_video(self) -> None:
        self.is_video = True
        print("📹 Видео записано!")

    def upload_video(self) -> None:
        self.is_video = True
        print("📂 Видео загружено!")

    def add_caption(self, text: str) -> None:
        if not text or not text.strip():
            raise ValueError("Caption cannot be empty")
        self.caption = text.strip()
        print(f'💬 Подпись добавлена: "{self.caption}"')

    def add_sticker(self, sticker_type: str = "emoji") -> None:
        self.has_sticker = True
        print(f"🖼️ Стикер '{sticker_type}' добавлен!")

    def apply_filter(self, filter_name: str) -> None:
        self.filter_applied = filter_name
        print(f"🎨 Фильтр '{filter_name}' применён!")

    def add_location(self, place: str) -> None:
        self.location = place.strip()
        print(f"📍 Местоположение добавлено: {self.location}")

    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at

    def publish_to_feed(self, feed: Feed) -> None:
        if self.is_expired():
            raise ValueError("Cannot publish expired story")
        feed.add_content(self)  # ← используем новый метод в Feed
        print("✅ История добавлена в ленту!")