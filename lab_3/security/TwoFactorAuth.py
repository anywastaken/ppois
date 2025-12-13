
import secrets
from datetime import datetime, timedelta

from social_network.exceptions.InvalidCredentialsException import InvalidCredentialsException


class TwoFactorAuth:

    # Хранилище активных токенов: {user_id: (token, expires_at)}
    _active_tokens: dict[int, tuple[str, datetime]] = {}

    @classmethod
    def generate_token(cls, user_id: int) -> str:

        token = f"{secrets.randbelow(1000000):06d}"  # 000000–999999
        expires_at = datetime.now() + timedelta(minutes=5)
        cls._active_tokens[user_id] = (token, expires_at)
        return token

    @classmethod
    def verify_token(cls, user_id: int, token: str) -> bool:

        if user_id not in cls._active_tokens:
            raise InvalidCredentialsException("No active 2FA token for this user")

        stored_token, expires_at = cls._active_tokens[user_id]

        # Удаляем токен сразу (чтобы нельзя было использовать повторно)
        del cls._active_tokens[user_id]

        if datetime.now() > expires_at:
            raise InvalidCredentialsException("2FA token has expired")

        if stored_token != token:
            raise InvalidCredentialsException("Invalid 2FA token")

        return True

    @classmethod
    def is_2fa_enabled_for_user(cls, user_id: int) -> bool:

        return user_id in cls._active_tokens