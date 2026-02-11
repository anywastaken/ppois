
from social_network.user.Profile import Profile


class GroupProfile(Profile):
    def __init__(self, group_id: int):
        super().__init__(group_id)
        self.group_id: int = group_id
        self.category: str | None = None
        self.rules: str | None = None
        self.is_closed: bool = False
        self.owner_id: int | None = None
        self.member_count: int = 0

    def set_category(self, category: str) -> None:
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")
        self.category = category.strip()

    def set_rules(self, rules: str) -> None:
        if rules and len(rules) > 2000:
            raise ValueError("Rules are too long (max 2000 characters)")
        self.rules = rules.strip() if rules else None

    def set_owner(self, owner_id: int) -> None:
        if owner_id <= 0:
            raise ValueError("Owner ID must be a positive integer")
        self.owner_id = owner_id

    def set_closed(self, is_closed: bool) -> None:
        self.is_closed = is_closed

    def update_group_statistics(self, followers: int, posts: int, members: int) -> None:
        self.update_statistics(followers, posts)
        if members < 0:
            raise ValueError("Member count cannot be negative")
        self.member_count = members

    def can_user_join(self, user_id: int) -> bool:
        if self.owner_id == user_id:
            return True
        if self.is_closed:
            return False
        return True