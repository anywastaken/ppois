
from social_network.database.Database import Database
from social_network.subscription.Subscription import Subscription


class SubscriptionDatabase(Database[Subscription, tuple[int, int, str]]):

    def _get_id(self, entity: Subscription) -> tuple[int, int, str]:
        """Составной ключ для подписки."""
        return entity.subscriber_id, entity.target_id, entity.target_type

    def subscribe(self, subscriber_id: int, target_id: int, target_type: str = "user") -> None:
        """Создаёт подписку."""
        subscription = Subscription(subscriber_id, target_id, target_type)
        self.add(subscription)

    def unsubscribe(self, subscriber_id: int, target_id: int, target_type: str = "user") -> bool:
        """Удаляет подписку. Возвращает True, если существовала."""
        key = (subscriber_id, target_id, target_type)
        return self.remove(key)

    def is_subscribed(self, subscriber_id: int, target_id: int, target_type: str = "user") -> bool:
        """Проверяет, подписан ли пользователь на цель."""
        key = (subscriber_id, target_id, target_type)
        return self.exists(key)

    def get_subscribers(self, target_id: int, target_type: str = "user") -> list[int]:
        """
        Возвращает список ID подписчиков цели (пользователя или группы).
        """
        return [
            sub.subscriber_id
            for sub in self._storage.values()
            if sub.target_id == target_id and sub.target_type == target_type
        ]

    def get_subscriptions(self, subscriber_id: int, target_type: str = "user") -> list[int]:
        """
        Возвращает список ID целей, на которые подписан пользователь (только указанного типа).
        """
        return [
            sub.target_id
            for sub in self._storage.values()
            if sub.subscriber_id == subscriber_id and sub.target_type == target_type
        ]

    def get_all_subscriptions_of_user(self, subscriber_id: int) -> list[Subscription]:
        """Возвращает все подписки пользователя (и на пользователей, и на группы)."""
        return [
            sub for sub in self._storage.values()
            if sub.subscriber_id == subscriber_id
        ]

    def get_subscriber_count(self, target_id: int, target_type: str = "user") -> int:
        """Считает количество подписчиков цели."""
        return sum(
            1 for sub in self._storage.values()
            if sub.target_id == target_id and sub.target_type == target_type
        )

    def get_subscription_count(self, subscriber_id: int) -> int:
        """Считает, сколько всего подписок у пользователя."""
        return sum(1 for sub in self._storage.values() if sub.subscriber_id == subscriber_id)