import pytest
from social_network.community.ChannelProfile import ChannelProfile


@pytest.fixture
def profile():
    return ChannelProfile(channel_id=123)


def test_channel_profile_initialization(profile):
    assert profile.id == 123
    assert profile.channel_id == 123
    assert profile.category is None
    assert profile.is_verified is False
    assert profile.subscriber_count == 0
    assert profile.post_count == 0
    assert profile.display_name is None
    assert profile.bio is None


def test_set_display_name(profile):
    profile.set_display_name("Tech News")
    assert profile.display_name == "Tech News"


def test_set_bio(profile):
    profile.set_bio("Latest in tech")
    assert profile.bio == "Latest in tech"


def test_set_category_success(profile):
    profile.set_category("technology")
    assert profile.category == "technology"


def test_set_category_empty_raises_error(profile):
    with pytest.raises(ValueError, match="Category cannot be empty"):
        profile.set_category("")
    with pytest.raises(ValueError, match="Category cannot be empty"):
        profile.set_category("   ")


def test_mark_as_verified(profile):
    profile.mark_as_verified()
    assert profile.is_verified is True


def test_update_channel_statistics_success(profile):
    profile.update_channel_statistics(subscribers=1500, posts=42)
    assert profile.subscriber_count == 1500
    assert profile.post_count == 42


def test_update_channel_statistics_negative_raises_error(profile):
    with pytest.raises(ValueError, match="Statistics cannot be negative"):
        profile.update_channel_statistics(subscribers=-1, posts=10)
    with pytest.raises(ValueError, match="Statistics cannot be negative"):
        profile.update_channel_statistics(subscribers=10, posts=-5)


def test_repr(profile):
    profile.set_display_name("News")
    assert "ChannelProfile(id=123, display_name='News')" in repr(profile)

    # Без имени
    empty_profile = ChannelProfile(999)
    assert "channel_999" in repr(empty_profile)