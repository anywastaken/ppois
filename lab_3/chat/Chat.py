
from abc import ABC
from datetime import datetime
from social_network.chat.Message import Message


class Chat(ABC):
    def __init__(self, chat_id: int):
        if chat_id <= 0:
            raise ValueError("Chat ID must be a positive integer")
        self.id: int = chat_id
        self._messages: list[Message] = []
        self.created_at: datetime = datetime.now()

    def send_message(self, sender_id: int, text: str) -> Message:
        """Отправляет сообщение в чат."""
        if not text or not text.strip():
            raise ValueError("Message text cannot be empty")
        message = Message(
            message_id=len(self._messages) + 1,
            chat_id=self.id,
            sender_id=sender_id,
            text=text
        )
        self._messages.append(message)
        return message

    def get_messages(self, limit: int | None = None) -> list[Message]:
        """Возвращает историю сообщений (новые в конце)."""
        if limit is None:
            return self._messages.copy()
        return self._messages[-limit:]  # последние N сообщений

    def get_message_count(self) -> int:
        """Возвращает количество сообщений."""
        return len(self._messages)

    def clear_history(self, user_id: int) -> None:
        """Очищает историю"""
        self._messages.clear()

    def find_message_by_id(self, message_id: int) -> Message | None:
        """Находит сообщение по ID."""
        for msg in self._messages:
            if msg.id == message_id:
                return msg
        return None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id}, messages={len(self._messages)})"