from typing import Set

from social_network.community.GroupProfile import GroupProfile
from social_network.content.Feed import Feed
from social_network.content.Post import Post
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException
from social_network.exceptions.UserNotFoundException import UserNotFoundException


class Group:
    def __init__(self, group_id: int, name: str, description: str, owner_id: int):
        if not name or not name.strip():
            raise ValueError("Group name cannot be empty")
        if group_id <= 0 or owner_id <= 0:
            raise ValueError("IDs must be positive integers")

        self.id: int = group_id
        self.name: str = name.strip()
        self.description: str = description.strip()
        self.owner_id: int = owner_id
        self._members: Set[int] = {owner_id}
        self._admins: Set[int] = {owner_id}
        self.feed: Feed = Feed(feed_id=group_id)

        self.profile:GroupProfile = GroupProfile(self.id)
        self.is_private: bool = False

    def _is_member(self, user_id: int) -> bool:
        return user_id in self._members

    def _is_admin(self, user_id: int) -> bool:
        return user_id in self._admins

    def _ensure_member(self, user_id: int) -> None:
        if not self._is_member(user_id):
            raise InsufficientPermissionsException("User is not a member of this group")

    def _ensure_admin(self, user_id: int) -> None:
        if not self._is_admin(user_id):
            raise InsufficientPermissionsException("User is not an admin of this group")

    def join(self, user_id: int) -> None:
        """Пользователь вступает в группу."""
        if user_id <= 0:
            raise ValueError("User ID must be positive")
        if self._is_member(user_id):
            raise ValueError("User is already a member")
        self._members.add(user_id)

    def leave(self, user_id: int) -> None:
        """Пользователь покидает группу."""
        if user_id == self.owner_id:
            raise ValueError("Owner cannot leave the group")
        if not self._is_member(user_id):
            raise UserNotFoundException("User is not a member")
        self._members.discard(user_id)
        self._admins.discard(user_id)  # если был админом — теряет права

    def add_admin(self, issuer_id: int, new_admin_id: int) -> None:
        """Назначает администратора (только админы могут)."""
        self._ensure_admin(issuer_id)
        if not self._is_member(new_admin_id):
            raise UserNotFoundException("User is not a member of the group")
        self._admins.add(new_admin_id)

    def remove_admin(self, issuer_id: int, admin_id: int) -> None:
        """Лишает прав администратора (кроме владельца)."""
        self._ensure_admin(issuer_id)
        if admin_id == self.owner_id:
            raise ValueError("Cannot remove owner's admin rights")
        self._admins.discard(admin_id)

    def create_post(self, author_id: int, content: str) -> Post:
        """Участник публикует пост в ленту группы."""
        self._ensure_member(author_id)
        post = Post(post_id=len(self.feed.get_items()) + 1, author_id=author_id, content=content)
        post.extract_and_store_hashtags()
        self.feed.add_post(post)
        return post

    def get_feed(self, viewer_id: int, limit: int | None = None) -> list:
        """
        Возвращает ленту постов.
        Доступ зависит от приватности:
        - публичная: любой может смотреть,
        - приватная: только участники.
        """
        if self.is_private and not self._is_member(viewer_id):
            raise InsufficientPermissionsException("This group is private")

        posts = self.feed.get_items(limit=limit)
        posts.sort(key=lambda p: p.created_at, reverse=True)
        return posts

    def delete_post(self, moderator_id: int, post_id: int) -> bool:
        """
        Удаляет пост из ленты группы.
        Может любой администратор или владелец.
        """
        self._ensure_admin(moderator_id)
        return self.feed.remove_post(post_id)

    def remove_member(self, moderator_id: int, user_id: int) -> None:
        """
        Удаляет пользователя из группы (и из админов).
        """
        self._ensure_admin(moderator_id)
        if user_id == self.owner_id:
            raise ValueError("Cannot remove the owner")
        if not self._is_member(user_id):
            raise UserNotFoundException("User is not a member")
        self._members.discard(user_id)
        self._admins.discard(user_id)

    def get_member_count(self) -> int:
        return len(self._members)

    def get_admin_count(self) -> int:
        return len(self._admins)

    def __repr__(self) -> str:
        return f"Group(id={self.id}, name='{self.name}', members={len(self._members)})"