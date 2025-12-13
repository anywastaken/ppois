import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
from social_network.recommendations.ReelsRecommendation import ReelsRecommendation
from social_network.recommendations.StoryRecommendations import StoryRecommendation
from social_network.database.ReelsDatabase import ReelsDatabase
from social_network.database.StoryDatabase import StoryDatabase
from social_network.content.Reels import Reels
from social_network.content.Story import Story


# === Вспомогательные фикстуры ===

@pytest.fixture
def reels_db():
    db = ReelsDatabase()
    r1 = Reels(1, 100)
    r1.record_video()
    r2 = Reels(2, 101)
    r2.record_video()
    r3 = Reels(3, 102)  # черновик (без видео)
    db.add(r1)
    db.add(r2)
    db.add(r3)
    return db


@pytest.fixture
def story_db():
    db = StoryDatabase()
    s1 = Story(1, 200)
    s1.record_video()

    s2 = Story(2, 201)
    s2.record_video()

    # Истёкшая история
    s3 = Story(3, 200)
    s3.record_video()
    s3.created_at = datetime.now() - timedelta(hours=25)
    s3.expires_at = s3.created_at + timedelta(hours=24)

    db.add(s1)
    db.add(s2)
    db.add(s3)
    return db


@pytest.fixture
def custom_reels():
    r = Reels(99, 50)
    r.record_video()
    return r


@pytest.fixture
def custom_story():
    s = Story(99, 60)
    s.record_video()
    return s


@pytest.fixture
def expired_story():
    s = Story(100, 70)
    s.record_video()
    s.created_at = datetime.now() - timedelta(hours=25)
    s.expires_at = s.created_at + timedelta(hours=24)
    return s


# === Тесты для ReelsRecommendation ===

def test_reels_recommendation_initialization():
    rec = ReelsRecommendation(feed_id=5)
    assert rec.id == 5
    assert rec._database is None


def test_reels_recommendation_set_database_success(reels_db):
    rec = ReelsRecommendation()
    rec.set_database(reels_db)
    assert rec._database is reels_db


def test_reels_recommendation_set_database_invalid_type():
    rec = ReelsRecommendation()
    with pytest.raises(TypeError, match="Database must be an instance of ReelsDatabase"):
        rec.set_database("not a database")


def test_reels_recommendation_add_content_success(custom_reels):
    rec = ReelsRecommendation()
    rec.add_content(custom_reels)
    assert len(rec._items) == 1


def test_reels_recommendation_add_content_invalid_type():
    rec = ReelsRecommendation()
    with pytest.raises(TypeError, match="ReelsRecommendation accepts only Reels instances"):
        rec.add_content("not a reels")


def test_reels_recommendation_add_post_blocked(custom_reels):
    rec = ReelsRecommendation()
    with pytest.raises(TypeError, match="ReelsRecommendation does not accept Posts"):
        rec.add_post("fake post")


def test_reels_recommendation_show_with_database(reels_db):
    rec = ReelsRecommendation()
    rec.set_database(reels_db)
    reels_list = rec.show(count=2)
    assert len(reels_list) == 2
    # Только опубликованные (r1, r2), не черновик (r3)
    assert all(r.is_video for r in reels_list)
    assert all(r.id in (1, 2) for r in reels_list)


def test_reels_recommendation_show_no_published_reels():
    db = ReelsDatabase()  # пустая база
    rec = ReelsRecommendation()
    rec.set_database(db)
    assert rec.show(count=1) == []


def test_reels_recommendation_show_fallback_to_custom(custom_reels):
    rec = ReelsRecommendation()
    rec.add_content(custom_reels)
    reels_list = rec.show(count=1)
    assert len(reels_list) == 1
    assert reels_list[0].id == 99


def test_reels_recommendation_show_mixed_custom_and_db(reels_db, custom_reels):
    rec = ReelsRecommendation()
    rec.set_database(reels_db)
    rec.add_content(custom_reels)
    # При наличии базы — использует ТОЛЬКО её
    reels_list = rec.show(count=3)
    assert all(r.id in (1, 2) for r in reels_list)


# === Тесты для StoryRecommendation ===

def test_story_recommendation_initialization():
    rec = StoryRecommendation(feed_id=10)
    assert rec.id == 10
    assert rec._database is None


def test_story_recommendation_set_database_success(story_db):
    rec = StoryRecommendation()
    rec.set_database(story_db)
    assert rec._database is story_db


def test_story_recommendation_set_database_invalid_type():
    rec = StoryRecommendation()
    with pytest.raises(TypeError, match="Database must be an instance of StoryDatabase"):
        rec.set_database("not a database")


def test_story_recommendation_add_content_success(custom_story):
    rec = StoryRecommendation()
    rec.add_content(custom_story)
    assert len(rec._items) == 1


def test_story_recommendation_add_expired_story_raises_error(expired_story):
    rec = StoryRecommendation()
    with pytest.raises(ValueError, match="Cannot add expired story to recommendation feed"):
        rec.add_content(expired_story)


def test_story_recommendation_add_content_invalid_type():
    rec = StoryRecommendation()
    with pytest.raises(TypeError, match="StoryRecommendation accepts only Story instances"):
        rec.add_content("not a story")


def test_story_recommendation_add_post_blocked():
    rec = StoryRecommendation()
    with pytest.raises(TypeError, match="StoryRecommendation does not accept Posts"):
        rec.add_post("fake post")


def test_story_recommendation_show_with_database(story_db):
    rec = StoryRecommendation()
    rec.set_database(story_db)
    stories = rec.show(count=2)
    assert len(stories) == 2
    # Только активные (s1, s2), не s3 (истёкшая)
    assert all(not s.is_expired() for s in stories)
    assert all(s.id in (1, 2) for s in stories)


def test_story_recommendation_show_no_active_stories():
    db = StoryDatabase()  # пустая база
    rec = StoryRecommendation()
    rec.set_database(db)
    assert rec.show(count=1) == []


def test_story_recommendation_show_fallback_to_custom(custom_story, expired_story):
    rec = StoryRecommendation()
    rec.add_content(custom_story)
    # Попытка добавить истёкшую — должна быть отклонена, но проверим только активную
    stories = rec.show(count=1)
    assert len(stories) == 1
    assert stories[0].id == 99
    assert not stories[0].is_expired()


def test_story_recommendation_show_only_active_from_custom(expired_story):
    rec = StoryRecommendation()
    # Добавляем ТОЛЬКО истёкшую — должна игнорироваться
    with pytest.raises(ValueError):
        rec.add_content(expired_story)
    assert rec.show(count=1) == []


# === Тесты на random.sample ===

def test_recommendations_use_random_sample(reels_db, story_db):
    """Проверяем, что используется random.sample (через mock)."""
    with patch('random.sample') as mock_sample:
        mock_sample.return_value = [Reels(1, 100)]

        rec = ReelsRecommendation()
        rec.set_database(reels_db)
        rec.show(1)
        mock_sample.assert_called()

    with patch('random.sample') as mock_sample:
        mock_sample.return_value = [Story(1, 200)]

        rec = StoryRecommendation()
        rec.set_database(story_db)
        rec.show(1)
        mock_sample.assert_called()


# === Тесты на __repr__ ===

def test_reels_recommendation_repr():
    rec = ReelsRecommendation(7)
    r = Reels(1, 100)
    r.record_video()
    rec.add_content(r)
    assert "ReelsRecommendation(id=7, items=1)" in repr(rec)


def test_story_recommendation_repr():
    rec = StoryRecommendation(8)
    s = Story(1, 200)
    s.record_video()
    rec.add_content(s)
    assert "StoryRecommendation(id=8, items=1)" in repr(rec)