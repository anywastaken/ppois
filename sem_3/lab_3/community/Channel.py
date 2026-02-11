
from typing import Set
from social_network.content.Feed import Feed
from social_network.content.Post import Post
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException
from social_network.community.ChannelProfile import ChannelProfile


class Channel:
    def __init__(self, channel_id: int, name: str, description: str, owner_id: int):
        if not name or not name.strip():
            raise ValueError("Channel name cannot be empty")
        if channel_id <= 0 or owner_id <= 0:
            raise ValueError("IDs must be positive integers")

        self.id: int = channel_id
        self.owner_id: int = owner_id
        self._subscribers: Set[int] = set()
        self._admins: Set[int] = {owner_id}
        self.feed: Feed = Feed(feed_id=channel_id)
        self.is_private: bool = False
        self.profile: ChannelProfile = ChannelProfile(channel_id)
        self.profile.set_display_name(name)
        self.profile.set_bio(description)

    def _is_subscriber(self, user_id: int) -> bool:
        return user_id in self._subscribers

    def _is_admin(self, user_id: int) -> bool:
        return user_id in self._admins

    def _ensure_admin(self, user_id: int) -> None:
        if not self._is_admin(user_id):
            raise InsufficientPermissionsException("Only admins can perform this action")


    def subscribe(self, user_id: int) -> None:
        if user_id <= 0 or user_id == self.owner_id:
            raise ValueError("Invalid user ID")
        self._subscribers.add(user_id)
        self.profile.subscriber_count = len(self._subscribers)

    def unsubscribe(self, user_id: int) -> None:
        if user_id not in self._subscribers:
            return
        self._subscribers.discard(user_id)
        self.profile.subscriber_count = len(self._subscribers)

    # === Управление админами ===

    def add_admin(self, issuer_id: int, new_admin_id: int) -> None:
        if issuer_id != self.owner_id:
            raise InsufficientPermissionsException("Only owner can appoint admins")
        if new_admin_id <= 0:
            raise ValueError("Admin ID must be positive")
        self._admins.add(new_admin_id)

    def remove_admin(self, issuer_id: int, admin_id: int) -> None:
        if issuer_id != self.owner_id:
            raise InsufficientPermissionsException("Only owner can remove admins")
        if admin_id == self.owner_id:
            raise ValueError("Cannot remove owner")
        self._admins.discard(admin_id)


    def create_post(self, author_id: int, content: str) -> Post:
        self._ensure_admin(author_id)
        post = Post(
            post_id=len(self.feed.get_items()) + 1,
            author_id=author_id,
            content=content
        )
        post.extract_and_store_hashtags()
        self.feed.add_content(post)
        self.profile.post_count += 1
        return post

    def get_feed(self, viewer_id: int, limit: int | None = None) -> list[Post]:
        if self.is_private and not (self._is_subscriber(viewer_id) or self._is_admin(viewer_id)):
            raise InsufficientPermissionsException("This channel is private")
        items = self.feed.get_items(limit=limit)
        posts = [item for item in items if isinstance(item, Post)]
        posts.sort(key=lambda p: p.created_at, reverse=True)
        return posts

    def delete_post(self, moderator_id: int, post_id: int) -> bool:
        self._ensure_admin(moderator_id)
        initial_count = len(self.feed._items)
        self.feed._items = [item for item in self.feed._items if getattr(item, 'id', None) != post_id]
        if len(self.feed._items) < initial_count:
            self.profile.post_count = len([i for i in self.feed._items if isinstance(i, Post)])
            return True
        return False

    def get_subscriber_count(self) -> int:
        return len(self._subscribers)

    def get_admin_count(self) -> int:
        return len(self._admins)

    def __repr__(self) -> str:
        return f"Channel(id={self.id}, name='{self.profile.display_name}', subscribers={len(self._subscribers)})"