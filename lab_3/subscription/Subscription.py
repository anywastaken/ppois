
from datetime import datetime


class Subscription:
    def __init__(self, subscriber_id: int, target_id: int, target_type: str = "user"):
        if subscriber_id <= 0 or target_id <= 0:
            raise ValueError("IDs must be positive integers")
        if subscriber_id == target_id and target_type == "user":
            raise ValueError("User cannot subscribe to themselves")
        if target_type not in {"user", "group"}:
            raise ValueError("Target type must be 'user' or 'group'")

        self.subscriber_id: int = subscriber_id
        self.target_id: int = target_id
        self.target_type: str = target_type
        self.created_at: datetime = datetime.now()

    def __eq__(self, other) -> bool:
        if isinstance(other, Subscription):
            return (
                self.subscriber_id == other.subscriber_id and
                self.target_id == other.target_id and
                self.target_type == other.target_type
            )
        return False

    def __hash__(self) -> int:
        return hash((self.subscriber_id, self.target_id, self.target_type))

    def __repr__(self) -> str:
        return f"Subscription(subscriber={self.subscriber_id}, target={self.target_id}, type={self.target_type})"