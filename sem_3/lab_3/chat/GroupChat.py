
from typing import Set
from social_network.chat.Chat import Chat
from social_network.chat.Message import Message
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException


class GroupChat(Chat):
    def __init__(self, chat_id: int, name: str, owner_id: int):
        super().__init__(chat_id)
        if not name or not name.strip():
            raise ValueError("Chat name cannot be empty")
        if owner_id <= 0:
            raise ValueError("Owner ID must be positive")

        self.name: str = name.strip()
        self.owner_id: int = owner_id
        self._participants: Set[int] = {owner_id}
        self._admins: Set[int] = {owner_id}

    def _is_participant(self, user_id: int) -> bool:
        return user_id in self._participants

    def _is_admin(self, user_id: int) -> bool:
        return user_id in self._admins

    def add_participant(self, issuer_id: int, user_id: int) -> None:
        """Добавляет участника (только админы)."""
        self._ensure_admin(issuer_id)
        if user_id <= 0:
            raise ValueError("User ID must be positive")
        self._participants.add(user_id)

    def remove_participant(self, issuer_id: int, user_id: int) -> None:
        """Удаляет участника (админы могут, владелец — всегда)."""
        if issuer_id != self.owner_id and not self._is_admin(issuer_id):
            raise InsufficientPermissionsException("Only admins can remove participants")
        if user_id == self.owner_id:
            raise ValueError("Cannot remove chat owner")
        self._participants.discard(user_id)
        self._admins.discard(user_id)  # теряет права админа

    def add_admin(self, issuer_id: int, user_id: int) -> None:
        """Назначает администратора (только владелец)."""
        if issuer_id != self.owner_id:
            raise InsufficientPermissionsException("Only owner can appoint admins")
        if not self._is_participant(user_id):
            raise ValueError("User must be a participant first")
        self._admins.add(user_id)

    def _ensure_admin(self, user_id: int) -> None:
        if not self._is_admin(user_id):
            raise InsufficientPermissionsException("User is not an admin")

    def send_message(self, sender_id: int, text: str) -> Message:
        if not self._is_participant(sender_id):
            raise InsufficientPermissionsException("User is not a participant of this group chat")
        return super().send_message(sender_id, text)

    def clear_history(self, user_id: int) -> None:
        """Очистка истории — только для админов."""
        if not self._is_admin(user_id):
            raise InsufficientPermissionsException("Only admins can clear history")
        super().clear_history(user_id)

    def get_participant_count(self) -> int:
        return len(self._participants)

    def get_admin_count(self) -> int:
        return len(self._admins)