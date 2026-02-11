import pytest
from social_network.user.User import User
from social_network.user.Profile import Profile
from social_network.user.UserProfile import UserProfile
from social_network.exceptions.EmptyUsernameError import EmptyUsernameError
from social_network.exceptions.PasswordTooWeakException import PasswordTooWeakException
from social_network.exceptions.AccountBannedException import AccountBannedException
from social_network.exceptions.InvalidCredentialsException import InvalidCredentialsException
from social_network.exceptions.TwoFactorRequiredException import TwoFactorRequiredException
from social_network.content.Post import Post


@pytest.fixture
def user():
    return User(1, "alice", "alice@example.com", "secure123")


@pytest.fixture
def profile():
    return Profile(1)


@pytest.fixture
def user_profile():
    return UserProfile(1)


def test_profile_initialization(profile):
    assert profile.id == 1
    assert profile.display_name is None
    assert profile.bio is None
    assert profile.follower_count == 0
    assert profile.post_count == 0


def test_profile_invalid_id():
    with pytest.raises(ValueError, match="Profile ID must be a positive integer"):
        Profile(0)
    with pytest.raises(ValueError, match="Profile ID must be a positive integer"):
        Profile(-1)


def test_set_display_name_success(profile):
    profile.set_display_name("Alice")
    assert profile.display_name == "Alice"


def test_set_display_name_empty(profile):
    with pytest.raises(ValueError, match="Display name cannot be empty"):
        profile.set_display_name("")
    with pytest.raises(ValueError, match="Display name cannot be empty"):
        profile.set_display_name("   ")


def test_set_display_name_too_long(profile):
    with pytest.raises(ValueError, match="Display name is too long"):
        profile.set_display_name("A" * 101)


def test_set_bio_success(profile):
    profile.set_bio("Hello world")
    assert profile.bio == "Hello world"


def test_set_bio_too_long(profile):
    with pytest.raises(ValueError, match="Bio is too long"):
        profile.set_bio("A" * 501)


def test_set_avatar_success(profile):
    profile.set_avatar("https://example.com/avatar.jpg")
    assert profile.avatar_url == "https://example.com/avatar.jpg"



def test_set_website_success(profile):
    profile.set_website("https://alice.com")
    assert profile.website == "https://alice.com"




def test_set_privacy(profile):
    profile.set_privacy(True)
    assert profile.is_private is True


def test_update_statistics_success(profile):
    profile.update_statistics(100, 50)
    assert profile.follower_count == 100
    assert profile.post_count == 50


def test_update_statistics_negative(profile):
    with pytest.raises(ValueError, match="Statistics values cannot be negative"):
        profile.update_statistics(-1, 10)
    with pytest.raises(ValueError, match="Statistics values cannot be negative"):
        profile.update_statistics(10, -1)


def test_user_initialization(user):
    assert user.id == 1
    assert user.username == "alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True
    assert user.two_factor_enabled is False


def test_user_empty_username():
    with pytest.raises(EmptyUsernameError, match="Username cannot be empty"):
        User(1, "", "test@example.com", "secure123")


def test_user_invalid_email():
    with pytest.raises(ValueError, match="Invalid email format"):
        User(1, "alice", "invalid-email", "secure123")


def test_user_weak_password():
    with pytest.raises(PasswordTooWeakException, match="Password must be at least 8 characters"):
        User(1, "alice", "alice@example.com", "123")


def test_authenticate_success(user):
    assert user.authenticate("secure123") is True


def test_authenticate_invalid_password(user):
    assert user.authenticate("wrong") is False


def test_authenticate_banned_account(user):
    user.is_active = False
    with pytest.raises(AccountBannedException, match="Account is deactivated"):
        user.authenticate("secure123")


def test_login_success(user):
    session = user.login("127.0.0.1")
    assert session.user_id == 1
    assert user.last_login is not None
    assert len(user.sessions) == 1


def test_login_banned_account(user):
    user.is_active = False
    with pytest.raises(AccountBannedException, match="Account is banned"):
        user.login("127.0.0.1")


def test_login_with_2fa_enabled(user):
    user.two_factor_enabled = True
    with pytest.raises(TwoFactorRequiredException, match="2FA is required"):
        user.login("127.0.0.1")


def test_change_password_success(user):
    user.change_password("secure123", "newpass123")
    assert user.authenticate("newpass123") is True


def test_change_password_wrong_old(user):
    with pytest.raises(InvalidCredentialsException, match="Current password is incorrect"):
        user.change_password("wrong", "newpass123")


def test_change_password_too_weak(user):
    with pytest.raises(PasswordTooWeakException, match="New password too weak"):
        user.change_password("secure123", "123")


def test_subscribe_to_self(user):
    with pytest.raises(ValueError, match="Cannot subscribe to yourself"):
        user.subscribe_to(1)


def test_create_post_success(user):
    post = user.create_post("Hello world")
    assert isinstance(post, Post)
    assert post.content == "Hello world"
    assert post.author_id == 1
    assert len(user.posts) == 1


def test_create_post_empty(user):
    with pytest.raises(ValueError, match="Post content cannot be empty"):
        user.create_post("")


def test_disable_account(user):
    user.disable_account()
    assert user.is_active is False


def test_enable_two_factor_auth(user):
    user.enable_two_factor_auth()
    assert user.two_factor_enabled is True


def test_get_active_session_count(user):
    user.login("127.0.0.1")
    assert user.get_active_session_count() == 1


def test_update_profile_bio(user):
    user.update_profile_bio("New bio")
    assert user.profile.bio == "New bio"


def test_user_profile_initialization(user_profile):
    assert user_profile.user_id == 1
    assert user_profile.allow_messages_from == "everyone"
    assert user_profile.following_count == 0


def test_set_message_permissions_success(user_profile):
    user_profile.set_message_permissions("followers")
    assert user_profile.allow_messages_from == "followers"


def test_set_message_permissions_invalid(user_profile):
    with pytest.raises(ValueError, match="Message permission must be one of"):
        user_profile.set_message_permissions("invalid")


def test_set_birth_date_success(user_profile):
    user_profile.set_birth_date(1990, 5, 15)
    assert user_profile.birth_date.year == 1990


def test_set_birth_date_invalid(user_profile):
    with pytest.raises(ValueError, match="Invalid date"):
        user_profile.set_birth_date(1990, 13, 1)


def test_set_location(user_profile):
    user_profile.set_location("Paris", "France")
    assert user_profile.city == "Paris"
    assert user_profile.country == "France"


def test_get_age(user_profile):
    user_profile.set_birth_date(1990, 1, 1)
    age = user_profile.get_age()
    assert age >= 34  # as of 2025


def test_get_age_future_date(user_profile):
    user_profile.set_birth_date(2026, 1, 1)
    assert user_profile.get_age() is None


def test_mark_as_verified(user_profile):
    user_profile.mark_as_verified()
    assert user_profile.is_verified is True


def test_update_user_statistics_success(user_profile):
    user_profile.update_user_statistics(100, 50, 30)
    assert user_profile.follower_count == 100
    assert user_profile.following_count == 50
    assert user_profile.post_count == 30


def test_update_user_statistics_negative_following(user_profile):
    with pytest.raises(ValueError, match="Following count cannot be negative"):
        user_profile.update_user_statistics(10, -1, 5)