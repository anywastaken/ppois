import pytest
from social_network.content.Hashtag import Hashtag


def test_hashtag_initialization_with_hash():
    """Тест инициализации с '#'."""
    tag = Hashtag("#Python")
    assert tag.tag == "python"
    assert tag.use_count == 1


def test_hashtag_initialization_without_hash():
    """Тест инициализации без '#'."""
    tag = Hashtag("pytest")
    assert tag.tag == "pytest"


def test_hashtag_empty_string_raises_error():
    """Тест ошибки при пустой строке."""
    with pytest.raises(ValueError, match="Hashtag cannot be empty"):
        Hashtag("")
    with pytest.raises(ValueError, match="Hashtag cannot be empty"):
        Hashtag("   ")


def test_hashtag_only_hash_raises_error():
    """Тест ошибки при только '#' или '#   '."""
    with pytest.raises(ValueError, match="Hashtag must contain non-whitespace characters after '#'"):
        Hashtag("#")
    with pytest.raises(ValueError, match="Hashtag must contain non-whitespace characters after '#'"):
        Hashtag("#   ")


def test_hashtag_invalid_characters():
    """Тест ошибки при недопустимых символах."""
    with pytest.raises(ValueError, match="Hashtag can only contain letters, digits, underscores and hyphens"):
        Hashtag("#hello!")
    with pytest.raises(ValueError, match="Hashtag can only contain letters, digits, underscores and hyphens"):
        Hashtag("#hello world")
    with pytest.raises(ValueError, match="Hashtag can only contain letters, digits, underscores and hyphens"):
        Hashtag("#hello@world")


def test_hashtag_valid_characters():
    """Тест допустимых символов: буквы, цифры, '_', '-'."""
    tag1 = Hashtag("#hello_world")
    assert tag1.tag == "hello_world"

    tag2 = Hashtag("#data-science123")
    assert tag2.tag == "data-science123"

    tag3 = Hashtag("#_test_")
    assert tag3.tag == "_test_"


def test_hashtag_case_insensitive():
    """Тест: хэштег всегда в нижнем регистре."""
    tag = Hashtag("#PyThOn")
    assert tag.tag == "python"


def test_increment_use_count():
    """Тест увеличения счётчика использования."""
    tag = Hashtag("#test")
    tag.increment_use_count()
    assert tag.use_count == 2
    tag.increment_use_count()
    assert tag.use_count == 3


def test_get_display_form():
    """Тест отображаемой формы."""
    tag = Hashtag("AI")
    assert tag.get_display_form() == "#ai"


def test_matches_success():
    """Тест совпадения тегов."""
    tag = Hashtag("#coding")
    assert tag.matches("#coding") is True
    assert tag.matches("coding") is True
    assert tag.matches("#CODING") is True
    assert tag.matches("CODING") is True


def test_matches_failure():
    """Тест несовпадения тегов."""
    tag = Hashtag("#python")
    assert tag.matches("#java") is False
    assert tag.matches("java") is False
    assert tag.matches("#python_") is False


def test_eq_and_hash():
    """Тест равенства и хеширования."""
    tag1 = Hashtag("#test")
    tag2 = Hashtag("test")
    tag3 = Hashtag("#Test")

    assert tag1 == tag2
    assert tag1 == tag3
    assert hash(tag1) == hash(tag2)
    assert hash(tag1) == hash(tag3)

    # Проверка использования в set
    tags = {tag1, tag2, tag3}
    assert len(tags) == 1


def test_repr():
    """Тест строкового представления."""
    tag = Hashtag("#SocialNetwork")
    assert repr(tag) == "Hashtag(tag='socialnetwork', uses=1)"