
from social_network.chat.Chat import Chat
from social_network.chat.Message import Message
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException


class PrivateChat(Chat):

    def __init__(self, chat_id: int, user1_id: int, user2_id: int):
        if user1_id <= 0 or user2_id <= 0:
            raise ValueError("User IDs must be positive integers")
        if user1_id == user2_id:
            raise ValueError("Cannot create private chat with yourself")

        super().__init__(chat_id)
        self.user1_id: int = user1_id
        self.user2_id: int = user2_id

    def _is_participant(self, user_id: int) -> bool:
        return user_id == self.user1_id or user_id == self.user2_id

    def send_message(self, sender_id: int, text: str) -> Message:
        if not self._is_participant(sender_id):
            raise InsufficientPermissionsException("User is not a participant of this private chat")
        return super().send_message(sender_id, text)

    def get_other_user_id(self, current_user_id: int) -> int:
        if current_user_id == self.user1_id:
            return self.user2_id
        elif current_user_id == self.user2_id:
            return self.user1_id
        else:
            raise ValueError("User is not a participant")

    def clear_history(self, user_id: int) -> None:
        if not self._is_participant(user_id):
            raise InsufficientPermissionsException("User is not a participant")
        super().clear_history(user_id)