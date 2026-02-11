
from datetime import datetime


class Message:

    def __init__(self, message_id: int, chat_id: int, sender_id: int, text: str):
        if message_id <= 0 or chat_id <= 0 or sender_id <= 0:
            raise ValueError("IDs must be positive integers")
        if not text or not text.strip():
            raise ValueError("Message text cannot be empty")

        self.id: int = message_id
        self.chat_id: int = chat_id
        self.sender_id: int = sender_id
        self.text: str = text.strip()
        self.sent_at: datetime = datetime.now()
        self.is_edited: bool = False

    def edit(self, new_text: str) -> None:
        if not new_text or not new_text.strip():
            raise ValueError("New message text cannot be empty")
        self.text = new_text.strip()
        self.is_edited = True

    def __repr__(self) -> str:
        return f"Message(id={self.id}, sender={self.sender_id}, text='{self.text[:30]}...')"