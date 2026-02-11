from social_network.database.Database import Database
from social_network.user.User import User


class UserDatabase(Database[User, int]):

    def _get_id(self, entity: User) -> int:
        """Извлекает ID из пользователя — требуется абстрактным Database."""
        return entity.id

    def get_by_username(self, username: str) -> User|None:
        """Возвращает пользователя по имени (точное совпадение)."""
        for user in self._storage.values():
            if user.username == username:
                return user
        return None

    def get_by_email(self, email: str) -> User|None:
        """Возвращает пользователя по email (точное совпадение)."""
        for user in self._storage.values():
            if user.email == email:
                return user
        return None

    def get_by_username_or_email(self, username_or_email: str) -> User|None:
        """Ищет пользователя по username ИЛИ email."""
        user = self.get_by_username(username_or_email)
        if user is not None:
            return user
        return self.get_by_email(username_or_email)

    def get_active_users(self) -> list[User]:
        """Возвращает всех активных (не заблокированных) пользователей."""
        return [user for user in self._storage.values() if user.is_active]

    def get_inactive_users(self) -> list[User]:
        """Возвращает всех неактивных (заблокированных) пользователей."""
        return [user for user in self._storage.values() if not user.is_active]

    def username_exists(self, username: str) -> bool:
        """Проверяет, занято ли имя пользователя."""
        return self.get_by_username(username) is not None

    def email_exists(self, email: str) -> bool:
        """Проверяет, зарегистрирован ли email."""
        return self.get_by_email(email) is not None

    def find_users_by_display_name(self, display_name: str) -> list[User]:
        """
        Ищет пользователей по отображаемому имени (в профиле).
        Возвращает совпадения по частичному вхождению (регистронезависимо).
        """
        display_name_lower = display_name.lower()
        result = []
        for user in self._storage.values():
            # Предполагается, что profile.display_name существует
            profile_name = getattr(user.profile, 'display_name', '')
            if profile_name and display_name_lower in profile_name.lower():
                result.append(user)
        return result

    def count_active_users(self) -> int:
        """Считает количество активных пользователей."""
        return sum(1 for user in self._storage.values() if user.is_active)

    def remove_user(self, user_id: int) -> bool:
        """
        Удаляет пользователя из базы.
        Возвращает True, если пользователь существовал.
        """
        if user_id in self._storage:
            del self._storage[user_id]
            return True
        return False