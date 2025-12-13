import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from social_network.security.AuthenticationManager import AuthenticationManager
from social_network.security.PasswordHasher import PasswordHasher
from social_network.security.TwoFactorAuth import TwoFactorAuth
from social_network.database.UserDatabase import UserDatabase
from social_network.user.User import User
from social_network.user.Profile import Profile
from social_network.session.Session import Session
from social_network.exceptions.InvalidCredentialsException import InvalidCredentialsException
from social_network.exceptions.UserNotFoundException import UserNotFoundException
from social_network.exceptions.TwoFactorRequiredException import TwoFactorRequiredException


@pytest.fixture
def user_db():
    db = UserDatabase()
    profile = Profile(1)
    user = User(1, "alice", "alice@example.com", "secure123")
    user.profile = profile
    db.add(user)
    return db


@pytest.fixture
def auth_manager(user_db):
    return AuthenticationManager(user_db)


def test_register_user(auth_manager, user_db):
    profile = Profile(2)
    new_user = User(2, "bob", "bob@example.com", "secure456")
    new_user.profile = profile
    auth_manager.register_user(new_user)
    assert user_db.get_by_id(2) is new_user


def test_authenticate_success(auth_manager):
    user = auth_manager.authenticate("alice", "secure123")
    assert user.username == "alice"


def test_authenticate_invalid_password(auth_manager):
    with pytest.raises(InvalidCredentialsException, match="Invalid password"):
        auth_manager.authenticate("alice", "wrong")


def test_authenticate_user_not_found(auth_manager):
    with pytest.raises(UserNotFoundException, match="User not found"):
        auth_manager.authenticate("charlie", "password")


def test_login_success(auth_manager):
    session = auth_manager.login("alice", "secure123", "127.0.0.1", "TestAgent")
    assert isinstance(session, Session)
    assert session.user_id == 1


def test_login_with_2fa_enabled(auth_manager, user_db):
    user = user_db.get_by_id(1)
    user.two_factor_enabled = True
    with pytest.raises(TwoFactorRequiredException, match="2FA token required"):
        auth_manager.login("alice", "secure123", "127.0.0.1")



def test_complete_2fa_login_2fa_not_enabled(auth_manager):
    with pytest.raises(InvalidCredentialsException, match="2FA is not enabled"):
        auth_manager.complete_2fa_login("alice", "secure123", "123456", "127.0.0.1")


def test_get_user_by_id_success(auth_manager):
    user = auth_manager.get_user_by_id(1)
    assert user.id == 1


def test_get_user_by_id_not_found(auth_manager):
    with pytest.raises(UserNotFoundException, match="User with ID 999 not found"):
        auth_manager.get_user_by_id(999)


def test_logout_user(auth_manager, user_db):
    user = user_db.get_by_id(1)
    session = user.login("127.0.0.1")
    auth_manager.logout_user(1)
    assert session.is_active is False



def test_password_hasher_hash_and_verify():
    hasher = PasswordHasher()
    hashed = hasher.hash("password123")
    assert hasher.verify("password123", hashed) is True
    assert hasher.verify("wrong", hashed) is False


def test_two_factor_auth_generate_and_verify():
    token = TwoFactorAuth.generate_token(1)
    assert len(token) == 6
    assert token.isdigit()
    assert TwoFactorAuth.verify_token(1, token) is True


def test_two_factor_auth_verify_invalid_token():
    TwoFactorAuth.generate_token(2)
    with pytest.raises(InvalidCredentialsException, match="Invalid 2FA token"):
        TwoFactorAuth.verify_token(2, "000000")


def test_two_factor_auth_verify_expired_token():
    with patch('social_network.security.TwoFactorAuth.datetime') as mock_dt:
        mock_dt.now.return_value = datetime(2025, 1, 1, 12, 0, 0)
        token = TwoFactorAuth.generate_token(3)

        mock_dt.now.return_value = datetime(2025, 1, 1, 12, 10, 0)
        with pytest.raises(InvalidCredentialsException, match="2FA token has expired"):
            TwoFactorAuth.verify_token(3, token)


def test_two_factor_auth_verify_nonexistent_user():
    with pytest.raises(InvalidCredentialsException, match="No active 2FA token"):
        TwoFactorAuth.verify_token(999, "123456")