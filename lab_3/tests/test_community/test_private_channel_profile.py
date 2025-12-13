import pytest
from social_network.community.PrivateChannelProfile import PrivateChannelProfile


@pytest.fixture
def profile():
    return PrivateChannelProfile(channel_id=777)


def test_private_channel_profile_initialization(profile):
    assert profile.id == 777
    assert profile.channel_id == 777
    assert profile.subscriber_count == 0
    assert profile.post_count == 0
    assert profile.is_verified is False


def test_set_category_success(profile):
    profile.set_category("exclusive")
    assert profile.category == "exclusive"


def test_mark_as_verified(profile):
    profile.mark_as_verified()
    assert profile.is_verified is True


def test_update_statistics_success(profile):
    profile.update_channel_statistics(subscribers=100, posts=10)
    assert profile.subscriber_count == 100
    assert profile.post_count == 10


def test_repr(profile):
    profile.set_display_name("VIP")
    assert "ChannelProfile(id=777, display_name='VIP')" in repr(profile)