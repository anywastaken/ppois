import pytest
from datetime import datetime, timedelta
from social_network.content.ContentItem import ContentItem
from social_network.content.Reels import Reels
from social_network.content.Feed import Feed
from unittest.mock import patch


# Вспомогательный класс для тестирования абстрактного ContentItem
class ConcreteContent(ContentItem):
    pass


@pytest.fixture
def content_item():
    return ConcreteContent(item_id=1, author_id=100)


@pytest.fixture
def reels():
    return Reels(reels_id=5, author_id=200)


@pytest.fixture
def feed():
    return Feed(feed_id=10)


# === Тесты для ContentItem ===

def test_content_item_initialization(content_item):
    assert content_item.id == 1
    assert content_item.author_id == 100
    assert isinstance(content_item.created_at, datetime)


def test_content_item_invalid_ids():
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        ConcreteContent(item_id=0, author_id=100)
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        ConcreteContent(item_id=1, author_id=-5)


def test_is_recent_true(content_item):
    # Только что создан → точно recent
    assert content_item.is_recent(hours=1) is True



def test_repr_content_item(content_item):
    assert repr(content_item) == "ConcreteContent(id=1, author_id=100)"


# === Тесты для Reels ===

def test_reels_initialization(reels):
    assert reels.id == 5
    assert reels.author_id == 200
    assert reels.is_video is False
    assert reels.caption is None
    assert reels.music_track is None
    assert reels.allow_comments is True
    assert reels.allow_duet is True


def test_record_video(reels):
    reels.record_video()
    assert reels.is_video is True


def test_upload_video(reels):
    reels.upload_video()
    assert reels.is_video is True


def test_add_caption_success(reels):
    reels.add_caption("Amazing sunset!")
    assert reels.caption == "Amazing sunset!"


def test_add_caption_empty_raises_error(reels):
    with pytest.raises(ValueError, match="Caption cannot be empty"):
        reels.add_caption("")
    with pytest.raises(ValueError, match="Caption cannot be empty"):
        reels.add_caption("   ")


def test_add_music(reels):
    # Создаём mock-трек (или можно сделать настоящий, если MusicTrack простой)
    class MockTrack:
        def __init__(self):
            self.artist = "Artist"
            self.title = "Song"
            self.use_count = 0

        def increment_use_count(self):
            self.use_count += 1

    track = MockTrack()
    reels.add_music(track)
    assert reels.music_track == "Artist — Song"
    assert track.use_count == 1


def test_apply_effects(reels):
    reels.apply_effects()
    assert reels.has_effects is True


def test_set_speed_success(reels):
    reels.set_speed(1.5)
    assert reels.has_speed_control is True


def test_set_speed_invalid(reels):
    with pytest.raises(ValueError, match="Speed must be positive"):
        reels.set_speed(0)
    with pytest.raises(ValueError, match="Speed must be positive"):
        reels.set_speed(-1.0)


def test_add_location(reels):
    reels.add_location("Paris, France")
    assert reels.location == "Paris, France"


def test_disable_comments(reels):
    reels.disable_comments()
    assert reels.allow_comments is False


def test_disable_duet(reels):
    reels.disable_duet()
    assert reels.allow_duet is False


def test_publish_to_feed_success(reels, feed):
    reels.record_video()  # чтобы is_video = True
    reels.publish_to_feed(feed)
    assert len(feed.get_items()) == 1
    assert feed.get_items()[0] is reels


def test_publish_without_video_fails(reels, feed):
    with pytest.raises(ValueError, match="Cannot publish Reels without video"):
        reels.publish_to_feed(feed)


def test_publish_to_non_feed_fails(reels):
    reels.record_video()
    with pytest.raises(TypeError, match="Feed must be an instance of Feed"):
        reels.publish_to_feed("not a feed")


def test_repr_reels(reels):
    # Черновик
    assert "черновик" in repr(reels)
    # После записи видео
    reels.record_video()
    assert "видео" in repr(reels)