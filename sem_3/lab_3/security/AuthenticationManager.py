

from datetime import datetime
from social_network.database.UserDatabase import UserDatabase
from social_network.user.User import User
from social_network.session.Session import Session
from social_network.security.TwoFactorAuth import TwoFactorAuth

from social_network.exceptions.InvalidCredentialsException import InvalidCredentialsException
from social_network.exceptions.UserNotFoundException import UserNotFoundException
from social_network.exceptions.TwoFactorRequiredException import TwoFactorRequiredException


class AuthenticationManager:
    def __init__(self, user_db: UserDatabase):
        self._db = user_db

    def register_user(self, user: User) -> None:
        """Регистрирует пользователя через базу данных."""
        self._db.add(user)

    def authenticate(self, username_or_email: str, password: str) -> User:
        """Аутентифицирует пользователя."""
        user = self._db.get_by_username_or_email(username_or_email)
        if user is None:
            raise UserNotFoundException("User not found")

        if not user.authenticate(password):
            raise InvalidCredentialsException("Invalid password")

        return user

    def login(self, username_or_email: str, password: str, ip_address: str, user_agent: str = "") -> Session:
        """Вход в систему."""
        user = self.authenticate(username_or_email, password)

        if user.two_factor_enabled:
            token = TwoFactorAuth.generate_token(user.id)
            print(f"[2FA] Generated token for {user.username}: {token}")
            raise TwoFactorRequiredException("2FA token required. Check your messages.")

        return user.login(ip_address, user_agent)

    def complete_2fa_login(
        self,
        username_or_email: str,
        password: str,
        token: str,
        ip_address: str,
        user_agent: str = ""
    ) -> Session:
        """Завершает вход с 2FA."""
        user = self.authenticate(username_or_email, password)

        if not user.two_factor_enabled:
            raise InvalidCredentialsException("2FA is not enabled for this account")

        if not TwoFactorAuth.verify_token(user.id, token):
            raise InvalidCredentialsException("Invalid or expired 2FA token")

        return user.login(ip_address, user_agent)

    def get_user_by_id(self, user_id: int) -> User:
        """Получает пользователя из БД."""
        user = self._db.get_by_id(user_id)
        if user is None:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return user

    def logout_user(self, user_id: int) -> None:
        """Завершает все сессии пользователя."""
        user = self.get_user_by_id(user_id)
        for session in user.sessions:
            session.is_active = False

    def is_session_valid(self, session: Session) -> bool:
        """Проверяет валидность сессии."""
        if not session.is_active:
            return False
        return datetime.now() < session.expires_at