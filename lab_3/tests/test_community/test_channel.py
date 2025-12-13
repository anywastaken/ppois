import pytest
from social_network.community.Channel import Channel
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException
from social_network.exceptions.UserNotFoundException import UserNotFoundException


@pytest.fixture
def channel():
    return Channel(channel_id=1, name="News", description="Daily news", owner_id=100)


def test_channel_initialization(channel):
    assert channel.id == 1
    assert channel.owner_id == 100
    assert channel.profile.display_name == "News"
    assert channel.profile.bio == "Daily news"
    assert channel.get_subscriber_count() == 0
    assert channel.get_admin_count() == 1


def test_channel_invalid_name():
    with pytest.raises(ValueError, match="Channel name cannot be empty"):
        Channel(channel_id=1, name="", description="x", owner_id=100)


def test_channel_invalid_ids():
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Channel(channel_id=0, name="Test", description="x", owner_id=100)
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Channel(channel_id=1, name="Test", description="x", owner_id=0)


def test_subscribe_success(channel):
    channel.subscribe(user_id=200)
    assert 200 in channel._subscribers
    assert channel.profile.subscriber_count == 1


def test_subscribe_invalid_user_id(channel):
    with pytest.raises(ValueError, match="Invalid user ID"):
        channel.subscribe(user_id=0)
    with pytest.raises(ValueError, match="Invalid user ID"):
        channel.subscribe(user_id=100)  # нельзя подписаться на свой канал


def test_unsubscribe_non_subscriber(channel):
    channel.unsubscribe(999)  # должно молча игнорироваться
    assert channel.get_subscriber_count() == 0


def test_add_admin_success(channel):
    channel.add_admin(issuer_id=100, new_admin_id=200)
    assert 200 in channel._admins


def test_add_admin_by_non_owner_fails(channel):
    with pytest.raises(InsufficientPermissionsException, match="Only owner can appoint admins"):
        channel.add_admin(issuer_id=200, new_admin_id=300)


def test_create_post_by_admin_success(channel):
    channel.add_admin(issuer_id=100, new_admin_id=200)
    post = channel.create_post(author_id=200, content="Breaking news!")
    assert post.content == "Breaking news!"
    assert channel.profile.post_count == 1


def test_create_post_by_non_admin_fails(channel):
    with pytest.raises(InsufficientPermissionsException, match="Only admins can perform this action"):
        channel.create_post(author_id=200, content="Spam")


def test_get_feed_private_access_denied(channel):
    channel.is_private = True
    with pytest.raises(InsufficientPermissionsException, match="This channel is private"):
        channel.get_feed(viewer_id=999)


def test_get_feed_private_access_allowed_for_subscriber(channel):
    channel.is_private = True
    channel.subscribe(200)
    posts = channel.get_feed(viewer_id=200)
    assert isinstance(posts, list)


def test_delete_post_success(channel):
    channel.add_admin(100, 200)
    post = channel.create_post(200, "To delete")
    deleted = channel.delete_post(moderator_id=200, post_id=post.id)
    assert deleted is True
    assert channel.profile.post_count == 0


def test_delete_nonexistent_post(channel):
    channel.add_admin(100, 200)
    deleted = channel.delete_post(moderator_id=200, post_id=999)
    assert deleted is False