import pytest
from datetime import datetime
from social_network.content.Comment import Comment
from social_network.content.Like import Like


# === Тесты для Like ===

def test_like_initialization_post():
    """Тест лайка под постом."""
    like = Like(like_id=1, user_id=100, post_id=50)
    assert like.id == 1
    assert like.user_id == 100
    assert like.post_id == 50
    assert like.comment_id is None
    assert like.is_on_post() is True
    assert like.is_on_comment() is False
    assert like.get_target_id() == 50
    assert like.get_target_type() == "post"


def test_like_initialization_comment():
    """Тест лайка под комментарием."""
    like = Like(like_id=2, user_id=101, comment_id=25)
    assert like.comment_id == 25
    assert like.post_id is None
    assert like.is_on_comment() is True
    assert like.get_target_id() == 25
    assert like.get_target_type() == "comment"


def test_like_invalid_no_target():
    """Тест ошибки: не указан ни пост, ни комментарий."""
    with pytest.raises(ValueError, match="exactly one of"):
        Like(like_id=1, user_id=100)


def test_like_invalid_both_targets():
    """Тест ошибки: указаны и пост, и комментарий."""
    with pytest.raises(ValueError, match="exactly one of"):
        Like(like_id=1, user_id=100, post_id=10, comment_id=20)


def test_like_invalid_ids():
    """Тест ошибки при недопустимых ID."""
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Like(like_id=0, user_id=100, post_id=10)
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Like(like_id=1, user_id=0, post_id=10)


def test_like_repr():
    """Тест строкового представления."""
    like1 = Like(1, 100, post_id=50)
    like2 = Like(2, 101, comment_id=25)
    assert "Like(id=1, user_id=100, on_post=50)" in repr(like1)
    assert "Like(id=2, user_id=101, on_comment=25)" in repr(like2)


# === Тесты для Comment ===

@pytest.fixture
def comment():
    return Comment(
        comment_id=10,
        post_id=100,
        author_id=50,
        text="Great post!"
    )


@pytest.fixture
def reply_comment():
    return Comment(
        comment_id=11,
        post_id=100,
        author_id=51,
        text="Thanks!",
        reply_to_comment_id=10
    )


def test_comment_initialization(comment):
    """Тест инициализации комментария."""
    assert comment.id == 10
    assert comment.post_id == 100
    assert comment.author_id == 50
    assert comment.text == "Great post!"
    assert comment.reply_to_comment_id is None
    assert comment.is_deleted is False
    assert comment.is_edited is False
    assert isinstance(comment.created_at, datetime)


def test_comment_initialization_reply(reply_comment):
    """Тест инициализации ответа на комментарий."""
    assert reply_comment.reply_to_comment_id == 10
    assert reply_comment.is_reply() is True


def test_comment_empty_text_raises_error():
    """Тест ошибки при пустом тексте."""
    with pytest.raises(ValueError, match="Comment text cannot be empty"):
        Comment(1, 100, 50, "")
    with pytest.raises(ValueError, match="Comment text cannot be empty"):
        Comment(1, 100, 50, "   ")


def test_comment_invalid_ids():
    """Тест ошибки при недопустимых ID."""
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Comment(0, 100, 50, "text")
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Comment(1, 0, 50, "text")
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Comment(1, 100, 0, "text")




def test_add_duplicate_like_raises_error(comment):
    """Тест ошибки при повторном лайке."""
    comment.add_like(200)
    with pytest.raises(ValueError, match="User already liked this comment"):
        comment.add_like(200)


def test_remove_like_success(comment):
    """Тест удаления лайка."""
    comment.add_like(200)
    removed = comment.remove_like(200)
    assert removed is True
    assert comment.get_like_count() == 0
    assert comment.is_liked_by(200) is False


def test_remove_nonexistent_like(comment):
    """Тест удаления несуществующего лайка."""
    removed = comment.remove_like(999)
    assert removed is False


def test_edit_comment_success(comment):
    """Тест успешного редактирования."""
    comment.edit("Updated comment!")
    assert comment.text == "Updated comment!"
    assert comment.is_edited is True
    assert isinstance(comment.updated_at, datetime)


def test_edit_comment_empty_text_raises_error(comment):
    """Тест ошибки при попытке отредактировать в пустой текст."""
    with pytest.raises(ValueError, match="New comment text cannot be empty"):
        comment.edit("")
    with pytest.raises(ValueError, match="New comment text cannot be empty"):
        comment.edit("   ")


def test_delete_comment(comment):
    """Тест soft-delete комментария."""
    comment.add_like(200)
    comment.delete()
    assert comment.text == "[УДАЛЕНО]"
    assert comment.is_deleted is True
    assert comment.get_like_count() == 0  # лайки очищены


def test_is_reply(comment, reply_comment):
    """Тест метода is_reply()."""
    assert comment.is_reply() is False
    assert reply_comment.is_reply() is True


def test_repr_comment(comment):
    """Тест строкового представления."""
    short = Comment(1, 10, 20, "Short")
    long = Comment(2, 10, 20, "A" * 50)
    assert "Short" in repr(short)
    assert "AAA..." in repr(long)


# === Интеграционный тест: Comment + Like ===

def test_comment_like_integration():
    """Тест взаимодействия комментария и лайка."""
    comment = Comment(1, 100, 50, "Hello")
    like = comment.add_like(99)

    # Проверяем, что лайк действительно привязан к комментарию
    assert like.is_on_comment() is True
    assert like.get_target_id() == comment.id
    assert like.comment_id == comment.id

    # Удаляем лайк
    assert comment.remove_like(99) is True
    assert comment.get_like_count() == 0