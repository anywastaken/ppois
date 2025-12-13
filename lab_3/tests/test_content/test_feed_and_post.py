import pytest
from social_network.content.Feed import Feed
from social_network.content.Post import Post
from social_network.content.ContentItem import ContentItem
from social_network.content.Comment import Comment
from social_network.content.Like import Like
from social_network.content.Hashtag import Hashtag
from social_network.media.MediaFile import MediaFile


# Вспомогательный класс, если нужно тестировать общий ContentItem
class DummyContent(ContentItem):
    pass


@pytest.fixture
def feed():
    return Feed(feed_id=1)


@pytest.fixture
def post():
    return Post(post_id=10, author_id=100, content="Hello #world!")


# === Тесты для Feed ===

def test_feed_initialization(feed):
    assert feed.id == 1
    assert len(feed._items) == 0


def test_add_content_success(feed, post):
    feed.add_content(post)
    assert len(feed._items) == 1
    assert feed._items[0] is post


def test_add_content_invalid_type(feed):
    with pytest.raises(TypeError, match="Only ContentItem instances can be added to Feed"):
        feed.add_content("not a content item")


def test_add_post_alias(feed, post):
    feed.add_post(post)
    assert len(feed._items) == 1


def test_get_items(feed, post):
    feed.add_content(post)
    items = feed.get_items()
    assert items == [post]
    assert items is not feed._items  # копия


def test_get_items_with_limit(feed):
    p1 = Post(1, 100, "A")
    p2 = Post(2, 101, "B")
    p3 = Post(3, 102, "C")
    feed.add_content(p1)
    feed.add_content(p2)
    feed.add_content(p3)

    limited = feed.get_items(limit=2)
    assert len(limited) == 2
    assert limited == [p1, p2]  # первые 2 ([:limit])


def test_get_posts(feed, post):
    feed.add_content(post)
    story = DummyContent(2, 200)
    feed.add_content(story)

    posts = feed.get_posts()
    assert len(posts) == 1
    assert posts[0] is post


def test_get_posts_with_limit(feed):
    for i in range(5):
        feed.add_content(Post(i+1, 100, f"Post {i}"))
    posts = feed.get_posts(limit=3)
    assert len(posts) == 3
    # последние 3 поста
    assert [p.id for p in posts] == [3, 4, 5]


def test_remove_post_success(feed, post):
    feed.add_content(post)
    assert feed.remove_post(post_id=10) is True
    assert len(feed._items) == 0


def test_remove_post_nonexistent(feed):
    assert feed.remove_post(post_id=999) is False


def test_remove_post_ignores_non_post_items(feed):
    dummy = DummyContent(99, 1)
    feed.add_content(dummy)
    assert feed.remove_post(post_id=99) is False  # не пост → не удаляется
    assert len(feed._items) == 1


def test_get_item_count(feed, post):
    assert feed.get_item_count() == 0
    feed.add_content(post)
    assert feed.get_item_count() == 1


def test_clear(feed, post):
    feed.add_content(post)
    feed.clear()
    assert len(feed._items) == 0


def test_len_and_iter(feed, post):
    feed.add_content(post)
    assert len(feed) == 1
    items = list(feed)
    assert items == [post]


def test_repr(feed, post):
    feed.add_content(post)
    assert "Feed(id=1, items=1)" in repr(feed)


# === Тесты для Post ===



def test_post_empty_content_raises_error():
    with pytest.raises(ValueError, match="Post content cannot be empty"):
        Post(1, 100, "")
    with pytest.raises(ValueError, match="Post content cannot be empty"):
        Post(1, 100, "   ")


def test_add_comment_success(post):
    comment = post.add_comment(author_id=200, text="Nice!")
    assert comment.author_id == 200
    assert comment.text == "Nice!"
    assert comment.post_id == post.id
    assert len(post.comments) == 1


def test_add_like_success(post):
    like = post.add_like(user_id=300)
    assert like.user_id == 300
    assert like.post_id == post.id
    assert post.likes_count == 1
    assert post.is_liked_by(300) is True


def test_add_duplicate_like_raises_error(post):
    post.add_like(300)
    with pytest.raises(ValueError, match="User already liked this post"):
        post.add_like(300)


def test_edit_content_empty_raises_error(post):
    with pytest.raises(ValueError, match="New content cannot be empty"):
        post.edit_content("")



def test_delete_post(post):
    post.add_like(300)
    post.add_comment(200, "Hi")
    post.delete()
    assert post.content == "[DELETED]"
    assert len(post.likes) == 0
    assert len(post.comments) == 0
    assert post.likes_count == 0
    assert len(post.hashtags) == 0


def test_get_comment_count(post):
    assert post.get_comment_count() == 0
    post.add_comment(200, "A")
    post.add_comment(201, "B")
    assert post.get_comment_count() == 2


def test_is_liked_by(post):
    assert post.is_liked_by(999) is False
    post.add_like(999)
    assert post.is_liked_by(999) is True


# === Интеграционные тесты ===

def test_feed_and_post_integration():
    feed = Feed(1)
    post = Post(1, 100, "Test post #demo")

    # Публикуем
    feed.add_post(post)
    assert len(feed.get_posts()) == 1

    # Удаляем
    assert feed.remove_post(1) is True
    assert len(feed.get_posts()) == 0
