
from social_network.user.Profile import Profile


class ChannelProfile(Profile):
    def __init__(self, channel_id: int):
        super().__init__(channel_id)
        self.channel_id: int = channel_id

        self.category: str | None = None
        self.is_verified: bool = False
        self.subscriber_count: int = 0
        self.post_count: int = 0

    def set_category(self, category: str) -> None:
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        self.category = category.strip()

    def mark_as_verified(self) -> None:
        self.is_verified = True

    def update_channel_statistics(self, subscribers: int, posts: int) -> None:
        if subscribers < 0 or posts < 0:
            raise ValueError("Statistics cannot be negative")
        self.subscriber_count = subscribers
        self.post_count = posts

    def __repr__(self) -> str:
        name = self.display_name or f"channel_{self.id}"
        return f"ChannelProfile(id={self.id}, display_name='{name}')"