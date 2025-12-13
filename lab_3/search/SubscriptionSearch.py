
from typing import List
from social_network.search.Search import Search
from social_network.subscription.Subscription import Subscription
from social_network.database.SubscriptionDatabase import SubscriptionDatabase


class SubscriptionSearch(Search):
    def __init__(self, subscription_database: SubscriptionDatabase):
        if not isinstance(subscription_database, SubscriptionDatabase):
            raise TypeError("subscription_database must be an instance of SubscriptionDatabase")
        self._db = subscription_database

    def search(self, query: str, limit: int = 10) -> List[Subscription]:
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty")

        results = []

        # 1. Если запрос — число, ищем по subscriber_id
        if query.isdigit():
            subscriber_id = int(query)
            results = self._db.get_all_subscriptions_of_user(subscriber_id)

        # 2. Если запрос в формате "subscriber:123"
        elif query.startswith("subscriber:") and query[12:].isdigit():
            subscriber_id = int(query[12:])
            results = self._db.get_all_subscriptions_of_user(subscriber_id)

        # 3. Если запрос в формате "target:456"
        elif query.startswith("target:") and query[7:].isdigit():
            target_id = int(query[7:])
            # Ищем все подписки на эту цель (и пользователей, и групп)
            for sub in self._db.get_all():
                if sub.target_id == target_id:
                    results.append(sub)

        # 4. Если запрос в формате "type:user" или "type:group"
        elif query.startswith("type:"):
            target_type = query[5:].strip().lower()
            if target_type in {"user", "group"}:
                for sub in self._db.get_all():
                    if sub.target_type == target_type:
                        results.append(sub)
            else:
                raise ValueError("Target type must be 'user' or 'group'")

        else:
            # Неподдерживаемый формат — возвращаем пустой список
            return []

        # Ограничиваем лимит
        return results[:limit]

    def search_by_id(self, subscription_id: int) -> Subscription | None:
        """
        Ищет подписку по составному ID.
        Но так как ID подписки — это кортеж, этот метод не используется напрямую.
        Возвращаем None, так как однозначного ID нет.
        """
        # Примечание: Subscription использует составной ключ, поэтому поиск по одному int не имеет смысла.
        return None