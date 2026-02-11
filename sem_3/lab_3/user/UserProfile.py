
from datetime import datetime
from social_network.user.Profile import Profile
from social_network.content.Feed import Feed


class UserProfile(Profile):

    def __init__(self, user_id: int):
        super().__init__(user_id)
        self.user_id: int = user_id

        self.birth_date: datetime | None = None
        self.city: str | None = None
        self.country: str | None = None
        self.allow_messages_from: str = "everyone"  # "everyone", "followers", "nobody"
        self.is_verified: bool = False
        self.feed: Feed = Feed(feed_id=user_id)
        self.follower_count = 0
        self.following_count: int = 0

    def set_message_permissions(self, level: str) -> None:
        allowed = {"everyone", "followers", "nobody"}
        if level not in allowed:
            raise ValueError(f"Message permission must be one of: {allowed}")
        self.allow_messages_from = level

    def set_birth_date(self, year: int, month: int, day: int) -> None:
        try:
            self.birth_date = datetime(year=year, month=month, day=day)
        except ValueError as e:
            raise ValueError(f"Invalid date: {e}")

    def set_location(self, city: str | None = None, country: str | None = None) -> None:
        self.city = city.strip() if city else None
        self.country = country.strip() if country else None

    def get_age(self) -> int | None:
        if self.birth_date is None:
            return None
        today = datetime.today()
        age = today.year - self.birth_date.year
        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):
            age -= 1
        return age if age >= 0 else None

    def mark_as_verified(self) -> None:
        self.is_verified = True

    def update_user_statistics(self, followers: int, following: int, posts: int) -> None:
        self.update_statistics(followers, posts)
        if following < 0:
            raise ValueError("Following count cannot be negative")
        self.following_count = following