
class Hashtag:
    def __init__(self, tag: str):
        if not tag or not tag.strip():
            raise ValueError("Hashtag cannot be empty")
        clean_tag = tag.lstrip('#').strip()
        if not clean_tag:
            raise ValueError("Hashtag must contain non-whitespace characters after '#'")
        if not clean_tag.replace('_', '').replace('-', '').isalnum():
            raise ValueError("Hashtag can only contain letters, digits, underscores and hyphens")

        self.tag: str = clean_tag.lower()  # хранится в нижнем регистре
        self.use_count: int = 1  # сколько раз использован (можно обновлять в PostDatabase)

    def increment_use_count(self) -> None:
        """Увеличивает счётчик использования хэштега."""
        self.use_count += 1

    def get_display_form(self) -> str:
        """Возвращает хэштег в формате '#example' для отображения."""
        return f"#{self.tag}"

    def matches(self, other_tag: str) -> bool:
        """
        Проверяет, совпадает ли переданный тег (с или без '#') с этим хэштегом.
        """
        clean_other = other_tag.lstrip('#').strip().lower()
        return clean_other == self.tag

    def __eq__(self, other) -> bool:
        if isinstance(other, Hashtag):
            return self.tag == other.tag
        return False

    def __hash__(self) -> int:
        return hash(self.tag)

    def __repr__(self) -> str:
        return f"Hashtag(tag='{self.tag}', uses={self.use_count})"