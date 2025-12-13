import pytest
from social_network.database.SubscriptionDatabase import SubscriptionDatabase
from social_network.database.UserDatabase import UserDatabase
from social_network.subscription.Subscription import Subscription
from social_network.user.User import User
from social_network.user.Profile import Profile


@pytest.fixture
def subscription_db():
    return SubscriptionDatabase()


@pytest.fixture
def user_db():
    db = UserDatabase()
    # Создаём профиль
    profile1 = Profile(1)
    profile1.set_display_name("Alice Smith")
    # ✅ Используем raw_password (минимум 8 символов!)
    user1 = User(user_id=1, username="alice", email="alice@example.com", raw_password="secure123")
    user1.profile = profile1
    user1.is_active = True

    profile2 = Profile(2)
    profile2.set_display_name("Bob Johnson")
    user2 = User(user_id=2, username="bob", email="bob@example.com", raw_password="secure456")
    user2.profile = profile2
    user2.is_active = False  # заблокирован

    db.add(user1)
    db.add(user2)
    return db


# === Тесты для SubscriptionDatabase ===

def test_subscription_database_subscribe(subscription_db):
    subscription_db.subscribe(100, 200, "user")
    assert subscription_db.is_subscribed(100, 200, "user") is True


def test_subscription_database_subscribe_duplicate_raises_error(subscription_db):
    subscription_db.subscribe(1, 2, "user")
    with pytest.raises(Exception):  # EntityAlreadyExistsException
        subscription_db.subscribe(1, 2, "user")


def test_subscription_database_unsubscribe(subscription_db):
    subscription_db.subscribe(10, 20, "group")
    assert subscription_db.unsubscribe(10, 20, "group") is True
    assert subscription_db.is_subscribed(10, 20, "group") is False


def test_subscription_database_unsubscribe_nonexistent(subscription_db):
    assert subscription_db.unsubscribe(99, 100, "user") is False


def test_subscription_database_is_subscribed(subscription_db):
    subscription_db.subscribe(1, 2, "user")
    assert subscription_db.is_subscribed(1, 2, "user") is True
    assert subscription_db.is_subscribed(2, 1, "user") is False


def test_subscription_database_get_subscribers(subscription_db):
    subscription_db.subscribe(100, 50, "group")
    subscription_db.subscribe(101, 50, "group")
    subscription_db.subscribe(100, 60, "user")

    subscribers = subscription_db.get_subscribers(50, "group")
    assert set(subscribers) == {100, 101}


def test_subscription_database_get_subscriptions(subscription_db):
    subscription_db.subscribe(100, 50, "group")
    subscription_db.subscribe(100, 60, "user")
    subscription_db.subscribe(101, 50, "group")

    subscriptions = subscription_db.get_subscriptions(100, "group")
    assert subscriptions == [50]


def test_get_all_subscriptions_of_user(subscription_db):
    subscription_db.subscribe(100, 50, "group")
    subscription_db.subscribe(100, 60, "user")

    all_subs = subscription_db.get_all_subscriptions_of_user(100)
    assert len(all_subs) == 2
    ids = {sub.target_id for sub in all_subs}
    assert ids == {50, 60}


def test_get_subscriber_count(subscription_db):
    subscription_db.subscribe(1, 10, "user")
    subscription_db.subscribe(2, 10, "user")
    subscription_db.subscribe(1, 20, "group")

    assert subscription_db.get_subscriber_count(10, "user") == 2
    assert subscription_db.get_subscriber_count(20, "group") == 1


def test_get_subscription_count(subscription_db):
    subscription_db.subscribe(100, 1, "user")
    subscription_db.subscribe(100, 2, "user")
    subscription_db.subscribe(100, 3, "group")

    assert subscription_db.get_subscription_count(100) == 3


# === Тесты для UserDatabase ===

def test_user_database_get_by_username(user_db):
    user = user_db.get_by_username("alice")
    assert user is not None
    assert user.email == "alice@example.com"


def test_user_database_get_by_username_not_found(user_db):
    assert user_db.get_by_username("unknown") is None


def test_user_database_get_by_email(user_db):
    user = user_db.get_by_email("bob@example.com")
    assert user is not None
    assert user.username == "bob"


def test_user_database_get_by_username_or_email(user_db):
    user1 = user_db.get_by_username_or_email("alice")
    assert user1.username == "alice"

    user2 = user_db.get_by_username_or_email("bob@example.com")
    assert user2.username == "bob"


def test_user_database_get_active_users(user_db):
    active = user_db.get_active_users()
    assert len(active) == 1
    assert active[0].username == "alice"


def test_user_database_get_inactive_users(user_db):
    inactive = user_db.get_inactive_users()
    assert len(inactive) == 1
    assert inactive[0].username == "bob"


def test_user_database_username_exists(user_db):
    assert user_db.username_exists("alice") is True
    assert user_db.username_exists("charlie") is False


def test_user_database_email_exists(user_db):
    assert user_db.email_exists("bob@example.com") is True
    assert user_db.email_exists("charlie@example.com") is False


def test_user_database_find_users_by_display_name(user_db):
    users1 = user_db.find_users_by_display_name("Alice")
    assert len(users1) == 1
    assert users1[0].username == "alice"

    users2 = user_db.find_users_by_display_name("SMITH")
    assert len(users2) == 1

    users3 = user_db.find_users_by_display_name("Charlie")
    assert len(users3) == 0


def test_user_database_count_active_users(user_db):
    assert user_db.count_active_users() == 1


def test_user_database_remove_user(user_db):
    assert user_db.remove_user(1) is True
    assert user_db.get_by_id(1) is None
    assert user_db.remove_user(999) is False


# === Интеграционный тест: базовый CRUD ===

def test_database_inheritance():
    sub_db = SubscriptionDatabase()
    sub = Subscription(1, 2, "user")
    sub_db.add(sub)
    assert sub_db.get_by_id((1, 2, "user")) is sub
    assert sub_db.exists((1, 2, "user")) is True
    assert sub_db.remove((1, 2, "user")) is True

    user_db = UserDatabase()
    # ✅ Пароль должен быть >= 8 символов
    user = User(10, "testuser", "test@test.com", "longenough")
    user_db.add(user)
    assert user_db.get_by_id(10) is user
    assert user_db.remove_user(10) is True