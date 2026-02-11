import pytest
from datetime import datetime, timedelta
from unittest.mock import patch
from social_network.database.PostDatabase import PostDatabase
from social_network.database.ReelsDatabase import ReelsDatabase
from social_network.database.StoryDatabase import StoryDatabase
from social_network.content.Post import Post
from social_network.content.Reels import Reels
from social_network.content.Story import Story
from social_network.content.MusicTrack import MusicTrack


# === Вспомогательные фикстуры ===

@pytest.fixture
def post_db():
    db = PostDatabase()
    p1 = Post(1, 100, "Hello #world!")
    p2 = Post(2, 101, "Public post")
    p3 = Post(3, 100, "Private thought")
    p3.is_public = False
    db.add(p1)
    db.add(p2)
    db.add(p3)
    return db


@pytest.fixture
def reels_db():
    db = ReelsDatabase()
    r1 = Reels(1, 200)
    r1.record_video()
    r1.add_caption("Dance!")
    r1.add_music(MusicTrack(1, "Levitating", "Dua Lipa", 203))

    r2 = Reels(2, 201)
    r2.record_video()
    r2.add_location("Tokyo")

    r3 = Reels(3, 200)  # черновик (без видео)

    db.add(r1)
    db.add(r2)
    db.add(r3)
    return db


@pytest.fixture
def story_db():
    db = StoryDatabase()
    s1 = Story(1, 300)
    s1.record_video()

    s2 = Story(2, 301)
    s2.record_video()

    # Истёкшая история (подделаем время)
    s3 = Story(3, 300)
    s3.record_video()
    # сдвинем created_at на 25 часов назад
    s3.created_at = datetime.now() - timedelta(hours=25)
    s3.expires_at = s3.created_at + timedelta(hours=24)

    db.add(s1)
    db.add(s2)
    db.add(s3)
    return db


# === Тесты для PostDatabase ===

def test_post_database_get_posts_by_author(post_db):
    posts = post_db.get_posts_by_author(100)
    assert len(posts) == 2
    assert all(p.author_id == 100 for p in posts)


def test_post_database_get_public_posts(post_db):
    public = post_db.get_public_posts()
    assert len(public) == 2  # p1 и p2
    assert all(p.is_public for p in public)


def test_post_database_get_recent_posts(post_db):
    recent = post_db.get_recent_posts(limit=2)
    # сортировка по created_at, новые сверху
    assert len(recent) == 2


def test_post_database_count_posts_by_author(post_db):
    assert post_db.count_posts_by_author(100) == 2
    assert post_db.count_posts_by_author(999) == 0


def test_post_database_delete_post(post_db):
    assert post_db.delete_post(1) is True
    assert post_db.get_by_id(1) is None
    assert post_db.delete_post(999) is False


# === Тесты для ReelsDatabase ===

def test_reels_database_get_reels_by_author(reels_db):
    reels = reels_db.get_reels_by_author(200)
    assert len(reels) == 2  # r1 и r3 (даже черновик)


def test_reels_database_get_all_reels(reels_db):
    all_reels = reels_db.get_all_reels()
    assert len(all_reels) == 3


def test_reels_database_get_published_reels(reels_db):
    published = reels_db.get_published_reels()
    assert len(published) == 2  # r1 и r2
    assert all(r.is_video for r in published)


def test_reels_database_get_reels_with_music(reels_db):
    with_music = reels_db.get_reels_with_music("Levitating")
    assert len(with_music) == 1
    assert "Levitating" in with_music[0].music_track


def test_reels_database_get_reels_by_location(reels_db):
    by_loc = reels_db.get_reels_by_location("Tokyo")
    assert len(by_loc) == 1
    assert "Tokyo" in by_loc[0].location


def test_reels_database_get_recent_reels(reels_db):
    recent = reels_db.get_recent_reels(limit=2)
    assert len(recent) == 2
    assert all(r.is_video for r in recent)  # только опубликованные


def test_reels_database_count_reels_by_author(reels_db):
    assert reels_db.count_reels_by_author(200) == 2


def test_reels_database_count_total_published_reels(reels_db):
    assert reels_db.count_total_published_reels() == 2


def test_reels_database_delete_reels_by_author(reels_db):
    count = reels_db.delete_reels_by_author(200)
    assert count == 2  # r1 и r3 удалены
    assert reels_db.get_by_id(1) is None
    assert reels_db.get_by_id(3) is None
    assert reels_db.get_by_id(2) is not None  # у другого автора


# === Тесты для StoryDatabase ===

def test_story_database_get_stories_by_author(story_db):
    stories = story_db.get_stories_by_author(300)
    assert len(stories) == 2  # s1 и s3


def test_story_database_get_active_stories_by_author(story_db):
    active = story_db.get_active_stories_by_author(300)
    assert len(active) == 1  # только s1


def test_story_database_get_all_active_stories(story_db):
    active = story_db.get_all_active_stories()
    assert len(active) == 2  # s1 и s2


def test_story_database_get_expired_stories(story_db):
    expired = story_db.get_expired_stories()
    assert len(expired) == 1  # s3


def test_story_database_count_active_stories(story_db):
    assert story_db.count_active_stories() == 2


def test_story_database_delete_expired_stories(story_db):
    count = story_db.delete_expired_stories()
    assert count == 1
    assert story_db.get_by_id(3) is None
    assert story_db.get_by_id(1) is not None


def test_story_database_get_recent_stories(story_db):
    recent = story_db.get_recent_stories(limit=2)
    assert len(recent) == 2
    assert all(not s.is_expired() for s in recent)


def test_story_database_has_active_story(story_db):
    assert story_db.has_active_story(300) is True
    assert story_db.has_active_story(999) is False


# === Интеграционный тест: базовый CRUD ===

def test_database_inheritance():
    """Проверяем, что все базы наследуют базовый функционал Database."""
    post_db = PostDatabase()
    post = Post(10, 50, "Test")
    post_db.add(post)
    assert post_db.get_by_id(10) is post
    assert post_db.exists(10) is True
    assert post_db.remove(10) is True
    assert post_db.exists(10) is False