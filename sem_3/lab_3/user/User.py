

from datetime import datetime

from social_network.exceptions.InvalidCredentialsException import InvalidCredentialsException
from social_network.exceptions.AccountBannedException import AccountBannedException
from social_network.exceptions.TwoFactorRequiredException import TwoFactorRequiredException
from social_network.exceptions.PasswordTooWeakException import PasswordTooWeakException
from social_network.exceptions.EmptyUsernameError import EmptyUsernameError

from social_network.security.PasswordHasher import PasswordHasher
from social_network.user.UserProfile import UserProfile
from social_network.content.Post import Post
from social_network.subscription.Subscription import Subscription
from social_network.session.Session import Session


class User:
    def __init__(self, user_id: int, username: str, email: str, raw_password: str):
        if not username or not username.strip():
            raise EmptyUsernameError("Username cannot be empty")
        if "@" not in email:
            raise ValueError("Invalid email format")
        if len(raw_password) < 8:
            raise PasswordTooWeakException("Password must be at least 8 characters")

        self.id: int = user_id
        self.username: str = username
        self.email: str = email
        self._hasher = PasswordHasher()
        self.password_hash: str = self._hasher.hash(raw_password)
        self.is_active: bool = True
        self.created_at: datetime = datetime.now()
        self.last_login: datetime | None = None
        self.two_factor_enabled: bool = False
        self.profile: UserProfile = UserProfile(self.id)

        self.subscriptions: list[Subscription] = []
        self.posts: list[Post] = []
        self.sessions: list[Session] = []
        self._next_post_id: int = 1
        self.posts: list[Post] = []

    def authenticate(self, password: str) -> bool:
        if not self.is_active:
            raise AccountBannedException("Account is deactivated")
        return self._hasher.verify(password, self.password_hash)

    def login(self, ip_address: str, user_agent: str = "") -> Session:
        if not self.is_active:
            raise AccountBannedException("Account is banned")
        if self.two_factor_enabled:
            raise TwoFactorRequiredException("2FA is required")

        session = Session(self.id, ip_address, user_agent)
        self.sessions.append(session)
        self.last_login = datetime.now()
        return session

    def login_with_2fa(self, password: str, token: str, ip_address: str, user_agent: str = "") -> Session:
        from social_network.security.TwoFactorAuth import TwoFactorAuth

        if not self.authenticate(password):
            raise InvalidCredentialsException("Invalid password")
        if not TwoFactorAuth.verify_token(self.id, token):
            raise InvalidCredentialsException("Invalid 2FA token")

        session = Session(self.id, ip_address, user_agent)
        self.sessions.append(session)
        self.last_login = datetime.now()
        return session

    def change_password(self, old_password: str, new_password: str) -> None:
        if not self.authenticate(old_password):
            raise InvalidCredentialsException("Current password is incorrect")
        if len(new_password) < 8:
            raise PasswordTooWeakException("New password too weak")
        self.password_hash = self._hasher.hash(new_password)

    def subscribe_to(self, target_user_id: int) -> None:
        if target_user_id == self.id:
            raise ValueError("Cannot subscribe to yourself")
        sub = Subscription(self.id, target_user_id)
        self.subscriptions.append(sub)

    def create_post(self, content: str) -> Post:
        if not content or not content.strip():
            raise ValueError("Post content cannot be empty")
        post_id = self._next_post_id
        self._next_post_id += 1
        post = Post(post_id=post_id, author_id=self.id, content=content)
        post.extract_and_store_hashtags()
        self.posts.append(post)
        return post

    def disable_account(self) -> None:
        self.is_active = False

    def enable_two_factor_auth(self) -> None:
        self.two_factor_enabled = True

    def get_active_session_count(self) -> int:
        return len([s for s in self.sessions if s.is_active])

    def update_profile_bio(self, bio: str) -> None:
        self.profile.bio = bio[:500]