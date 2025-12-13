
from abc import ABC
from datetime import datetime


class Profile(ABC):

    def __init__(self, profile_id: int):
        if profile_id <= 0:
            raise ValueError("Profile ID must be a positive integer")

        self.id: int = profile_id
        self.display_name: str | None = None
        self.bio: str | None = None
        self.avatar_url: str | None = None
        self.website: str | None = None
        self.is_private: bool = False
        self.created_at: datetime = datetime.now()
        self.follower_count: int = 0
        self.post_count: int = 0

    def set_display_name(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("Display name cannot be empty")
        if len(name) > 100:
            raise ValueError("Display name is too long (max 100 characters)")
        self.display_name = name.strip()

    def set_bio(self, bio: str) -> None:
        if bio and len(bio) > 500:
            raise ValueError("Bio is too long (max 500 characters)")
        self.bio = bio.strip() if bio else None

    def set_avatar(self, avatar_url: str) -> None:
        if not avatar_url or not avatar_url.strip():
            raise ValueError("Avatar URL cannot be empty")
        if not (avatar_url.startswith("http://") or avatar_url.startswith("https://")):
            raise ValueError("Avatar URL must be a valid HTTP(S) URL")
        self.avatar_url = avatar_url.strip()

    def set_website(self, url: str) -> None:
        if url and not (url.startswith("http://") or url.startswith("https://")):
            raise ValueError("Website must be a valid HTTP(S) URL")
        self.website = url.strip() if url else None

    def set_privacy(self, is_private: bool) -> None:
        self.is_private = is_private

    def update_statistics(self, followers: int, posts: int) -> None:
        if followers < 0 or posts < 0:
            raise ValueError("Statistics values cannot be negative")
        self.follower_count = followers
        self.post_count = posts

    def __repr__(self) -> str:
        name = self.display_name or f"profile_{self.id}"
        return f"{self.__class__.__name__}(id={self.id}, display_name='{name}')"