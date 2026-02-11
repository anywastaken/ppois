import pytest
from social_network.community.PrivateChannel import PrivateChannel
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException


@pytest.fixture
def private_channel():
    return PrivateChannel(
        channel_id=5,
        name="VIP News",
        description="Exclusive content",
        owner_id=101
    )


def test_private_channel_initialization(private_channel):
    """Тест инициализации PrivateChannel."""
    assert private_channel.id == 5
    assert private_channel.owner_id == 101
    assert private_channel.profile.display_name == "VIP News"
    assert private_channel.profile.bio == "Exclusive content"
    assert private_channel.get_subscriber_count() == 0
    assert private_channel.get_admin_count() == 1
    # ✅ Теперь по умолчанию приватный
    assert private_channel.is_private is True


def test_private_channel_invalid_name():
    """Тест ошибки при пустом имени."""
    with pytest.raises(ValueError, match="Channel name cannot be empty"):
        PrivateChannel(1, "", "desc", 100)
    with pytest.raises(ValueError, match="Channel name cannot be empty"):
        PrivateChannel(1, "   ", "desc", 100)


def test_private_channel_invalid_ids():
    """Тест ошибки при недопустимых ID."""
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        PrivateChannel(0, "Test", "desc", 100)
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        PrivateChannel(1, "Test", "desc", 0)


def test_subscribe_success(private_channel):
    """Тест успешной подписки."""
    private_channel.subscribe(user_id=200)
    assert 200 in private_channel._subscribers
    assert private_channel.profile.subscriber_count == 1


def test_subscribe_owner_fails(private_channel):
    """Тест ошибки при попытке подписаться владельцем."""
    with pytest.raises(ValueError, match="Invalid user ID"):
        private_channel.subscribe(user_id=101)


def test_subscribe_invalid_user_id(private_channel):
    """Тест ошибки при недопустимом user_id."""
    with pytest.raises(ValueError, match="Invalid user ID"):
        private_channel.subscribe(user_id=0)
    with pytest.raises(ValueError, match="Invalid user ID"):
        private_channel.subscribe(user_id=-5)


def test_unsubscribe_non_subscriber(private_channel):
    """Отписка несуществующего подписчика — игнорируется."""
    private_channel.unsubscribe(999)
    assert private_channel.get_subscriber_count() == 0


def test_add_admin_success(private_channel):
    """Тест назначения админа владельцем."""
    private_channel.add_admin(issuer_id=101, new_admin_id=200)
    assert 200 in private_channel._admins


def test_add_admin_by_non_owner_fails(private_channel):
    """Тест ошибки при назначении не владельцем."""
    with pytest.raises(InsufficientPermissionsException, match="Only owner can appoint admins"):
        private_channel.add_admin(issuer_id=200, new_admin_id=300)


def test_create_post_by_admin_success(private_channel):
    """Тест публикации поста админом."""
    private_channel.add_admin(101, 200)
    post = private_channel.create_post(author_id=200, content="Secret update")
    assert post.content == "Secret update"
    assert private_channel.profile.post_count == 1


def test_create_post_by_non_admin_fails(private_channel):
    """Тест ошибки при публикации не админом."""
    with pytest.raises(InsufficientPermissionsException, match="Only admins can perform this action"):
        private_channel.create_post(author_id=200, content="Spam")


def test_get_feed_private_access_denied_for_non_subscriber(private_channel):
    """Тест: доступ к ленте запрещён неподписанным."""
    with pytest.raises(InsufficientPermissionsException, match="This channel is private"):
        private_channel.get_feed(viewer_id=999)


def test_get_feed_private_access_allowed_for_subscriber(private_channel):
    """Тест: подписчик может смотреть ленту."""
    private_channel.subscribe(200)
    posts = private_channel.get_feed(viewer_id=200)
    assert isinstance(posts, list)


def test_get_feed_private_access_allowed_for_admin(private_channel):
    """Тест: админ может смотреть ленту (даже без подписки)."""
    private_channel.add_admin(101, 200)
    posts = private_channel.get_feed(viewer_id=200)
    assert isinstance(posts, list)


def test_get_feed_private_access_allowed_for_owner(private_channel):
    """Тест: владелец всегда может смотреть ленту."""
    posts = private_channel.get_feed(viewer_id=101)
    assert isinstance(posts, list)


def test_delete_post_success(private_channel):
    """Тест успешного удаления поста."""
    private_channel.add_admin(101, 200)
    post = private_channel.create_post(200, "To delete")
    deleted = private_channel.delete_post(moderator_id=200, post_id=post.id)
    assert deleted is True
    assert private_channel.profile.post_count == 0


def test_delete_nonexistent_post(private_channel):
    """Тест удаления несуществующего поста."""
    private_channel.add_admin(101, 200)
    deleted = private_channel.delete_post(moderator_id=200, post_id=999)
    assert deleted is False


def test_repr(private_channel):
    """Тест строкового представления."""
    repr_str = repr(private_channel)
    assert "Channel(id=5, name='VIP News', subscribers=0)" in repr_str