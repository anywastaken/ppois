

from datetime import datetime
from urllib.parse import urlparse


class MediaFile:

    # Поддерживаемые типы медиа
    SUPPORTED_TYPES = {"image", "video", "audio", "document"}

    def __init__(
        self,
        media_id: int,
        file_url: str,
        media_type: str = "image",
        description: str | None = None,
        uploaded_by: int | None = None
    ):
        if media_id <= 0:
            raise ValueError("Media ID must be a positive integer")
        if not file_url or not file_url.strip():
            raise ValueError("File URL cannot be empty")
        if not self._is_valid_url(file_url):
            raise ValueError("Invalid file URL format")
        if media_type not in self.SUPPORTED_TYPES:
            raise ValueError(f"Unsupported media type: {media_type}. Supported: {self.SUPPORTED_TYPES}")

        self.id: int = media_id
        self.file_url: str = file_url.strip()
        self.media_type: str = media_type
        self.description: str | None = description.strip() if description else None
        self.uploaded_by: int | None = uploaded_by
        self.uploaded_at: datetime = datetime.now()
        self.file_size_bytes: int | None = None
        self.is_private: bool = False


    def _is_valid_url(self, url: str) -> bool:
        """Проверяет, что строка является корректным URL."""
        try:
            result = urlparse(url)
            return bool(result.scheme and result.netloc)
        except Exception:
            return False

    def set_file_size(self, size_bytes: int) -> None:
        if size_bytes < 0:
            raise ValueError("File size cannot be negative")
        self.file_size_bytes = size_bytes

    def make_private(self) -> None:
        self.is_private = True

    def make_public(self) -> None:
        self.is_private = False

    def get_file_extension(self) -> str | None:
        try:
            path = urlparse(self.file_url).path
            if '.' in path:
                return path.rsplit('.', 1)[-1].lower()
            return None
        except Exception:
            return None

    def is_image(self) -> bool:
        return self.media_type == "image"

    def is_video(self) -> bool:
        return self.media_type == "video"

    def __repr__(self) -> str:
        return f"MediaFile(id={self.id}, type={self.media_type}, url='{self.file_url[:30]}...')"