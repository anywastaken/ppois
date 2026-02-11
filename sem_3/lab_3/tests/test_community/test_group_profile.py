import pytest
from social_network.community.GroupProfile import GroupProfile


@pytest.fixture
def profile():
    return GroupProfile(group_id=456)


def test_group_profile_initialization(profile):
    assert profile.id == 456
    assert profile.group_id == 456
    assert profile.category is None
    assert profile.rules is None
    assert profile.is_closed is False
    assert profile.owner_id is None
    assert profile.member_count == 0
    assert profile.display_name is None
    assert profile.bio is None


def test_set_category_success(profile):
    profile.set_category("hobby")
    assert profile.category == "hobby"


def test_set_category_empty_raises_error(profile):
    with pytest.raises(ValueError, match="Category cannot be empty"):
        profile.set_category("")
    with pytest.raises(ValueError, match="Category cannot be empty"):
        profile.set_category("   ")


def test_set_rules_success(profile):
    profile.set_rules("Be kind.")
    assert profile.rules == "Be kind."


def test_set_rules_long_raises_error(profile):
    long_rules = "x" * 2001
    with pytest.raises(ValueError, match="Rules are too long"):
        profile.set_rules(long_rules)


def test_set_rules_empty(profile):
    profile.set_rules("")
    assert profile.rules is None  # или "" — зависит от реализации
    # В вашем коде: `rules.strip() if rules else None` → None


def test_set_owner_success(profile):
    profile.set_owner(100)
    assert profile.owner_id == 100


def test_set_owner_invalid_id(profile):
    with pytest.raises(ValueError, match="Owner ID must be a positive integer"):
        profile.set_owner(0)
    with pytest.raises(ValueError, match="Owner ID must be a positive integer"):
        profile.set_owner(-5)


def test_set_closed(profile):
    profile.set_closed(True)
    assert profile.is_closed is True
    profile.set_closed(False)
    assert profile.is_closed is False


def test_update_group_statistics_success(profile):
    # Предполагаем, что Profile.update_statistics(followers, posts) существует
    profile.update_group_statistics(followers=1000, posts=50, members=200)
    assert profile.follower_count == 1000  # если у Profile есть follower_count
    assert profile.post_count == 50
    assert profile.member_count == 200


def test_update_group_statistics_negative_members_raises_error(profile):
    with pytest.raises(ValueError, match="Member count cannot be negative"):
        profile.update_group_statistics(followers=10, posts=5, members=-1)


def test_can_user_join_public_group(profile):
    profile.set_owner(100)
    assert profile.can_user_join(200) is True  # не владелец, группа открыта


def test_can_user_join_closed_group(profile):
    profile.set_owner(100)
    profile.set_closed(True)
    assert profile.can_user_join(200) is False


def test_can_user_join_as_owner(profile):
    profile.set_owner(100)
    profile.set_closed(True)
    assert profile.can_user_join(100) is True  # владелец всегда может


def test_repr(profile):
    profile.set_display_name("Gamers")
    assert "Profile" in repr(profile)  # зависит от реализации Profile.__repr__
    # Если вы хотите более точное представление — можно уточнить