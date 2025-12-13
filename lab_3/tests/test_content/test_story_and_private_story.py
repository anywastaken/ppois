import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from social_network.content.Story import Story
from social_network.content.PrivateStory import PrivateStory
from social_network.content.Feed import Feed


# Параметризация: запускаем один и тот же тест для Story и PrivateStory
@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_story_initialization(StoryClass):
    """Тест инициализации Story и PrivateStory."""
    story = StoryClass(story_id=1, author_id=100)
    assert story.id == 1
    assert story.author_id == 100
    assert story.is_video is False
    assert story.caption is None
    assert story.has_sticker is False
    assert story.filter_applied is None
    assert story.location is None
    assert isinstance(story.created_at, datetime)
    assert story.expires_at == story.created_at + timedelta(hours=24)


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_story_record_video(StoryClass):
    """Тест записи видео."""
    story = StoryClass(1, 100)
    story.record_video()
    assert story.is_video is True


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_story_upload_video(StoryClass):
    """Тест загрузки видео."""
    story = StoryClass(1, 100)
    story.upload_video()
    assert story.is_video is True


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_add_caption_success(StoryClass):
    """Тест добавления подписи."""
    story = StoryClass(1, 100)
    story.add_caption("Beautiful sunset!")
    assert story.caption == "Beautiful sunset!"


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_add_caption_empty_raises_error(StoryClass):
    """Тест ошибки при пустой подписи."""
    story = StoryClass(1, 100)
    with pytest.raises(ValueError, match="Caption cannot be empty"):
        story.add_caption("")
    with pytest.raises(ValueError, match="Caption cannot be empty"):
        story.add_caption("   ")


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_add_sticker(StoryClass):
    """Тест добавления стикера."""
    story = StoryClass(1, 100)
    story.add_sticker("poll")
    assert story.has_sticker is True


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_apply_filter(StoryClass):
    """Тест применения фильтра."""
    story = StoryClass(1, 100)
    story.apply_filter("Clarendon")
    assert story.filter_applied == "Clarendon"


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_add_location(StoryClass):
    """Тест добавления локации."""
    story = StoryClass(1, 100)
    story.add_location("Tokyo, Japan")
    assert story.location == "Tokyo, Japan"


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_is_expired_not_expired(StoryClass):
    """Тест: история не истекла."""
    story = StoryClass(1, 100)
    assert story.is_expired() is False


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_is_expired_expired(StoryClass):
    """Тест: история истекла (подделываем время)."""
    with patch('social_network.content.Story.datetime') as mock_dt1, \
         patch('social_network.content.PrivateStory.datetime') as mock_dt2:

        # Для обоих классов подделываем datetime.now()
        mock_dt1.now.return_value = datetime(2025, 12, 14, 0, 0, 0)
        mock_dt2.now.return_value = datetime(2025, 12, 14, 0, 0, 0)

        story = StoryClass(1, 100)
        # Устанавливаем created_at на 25 часов назад
        story.created_at = datetime(2025, 12, 12, 23, 0, 0)
        story.expires_at = story.created_at + timedelta(hours=24)

        assert story.is_expired() is True


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_publish_to_feed_success(StoryClass):
    """Тест успешной публикации в ленту."""
    story = StoryClass(1, 100)
    story.record_video()
    feed = Feed(feed_id=10)

    story.publish_to_feed(feed)

    assert len(feed.get_items()) == 1
    assert feed.get_items()[0] is story


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_publish_expired_story_fails(StoryClass):
    """Тест ошибки при публикации истёкшей истории."""
    with patch('social_network.content.Story.datetime') as mock_dt1, \
         patch('social_network.content.PrivateStory.datetime') as mock_dt2:

        mock_dt1.now.return_value = datetime(2025, 12, 14, 0, 0, 0)
        mock_dt2.now.return_value = datetime(2025, 12, 14, 0, 0, 0)

        story = StoryClass(1, 100)
        story.created_at = datetime(2025, 12, 12, 0, 0, 0)
        story.expires_at = story.created_at + timedelta(hours=24)  # 13 дек, 00:00

        feed = Feed(10)

        with pytest.raises(ValueError, match="Cannot publish expired story"):
            story.publish_to_feed(feed)


@pytest.mark.parametrize("StoryClass", [Story, PrivateStory])
def test_repr(StoryClass):
    """Тест строкового представления."""
    story = StoryClass(5, 200)
    repr_str = repr(story)
    assert f"{StoryClass.__name__}(id=5, author_id=200)" in repr_str