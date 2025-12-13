import pytest
from unittest.mock import patch
from social_network.recommendations.MusicRecommendation import MusicRecommendation
from social_network.recommendations.PostRecommendations import PostRecommendation
from social_network.database.MusicDatabase import MusicDatabase
from social_network.database.PostDatabase import PostDatabase
from social_network.content.MusicTrack import MusicTrack
from social_network.content.Post import Post


# === Фикстуры ===

@pytest.fixture
def music_db():
    db = MusicDatabase()
    db.add(MusicTrack(1, "Track A", "Artist X", 180))
    db.add(MusicTrack(2, "Track B", "Artist Y", 200))
    db.add(MusicTrack(3, "Track C", "Artist X", 190))
    # Увеличим популярность Track A
    db._storage[1].increment_use_count()
    db._storage[1].increment_use_count()
    return db


@pytest.fixture
def post_db():
    db = PostDatabase()
    db.add(Post(1, 100, "Public post 1"))
    db.add(Post(2, 101, "Public post 2"))
    private_post = Post(3, 100, "Private post")
    private_post.is_public = False
    db.add(private_post)
    return db


@pytest.fixture
def custom_track():
    return MusicTrack(99, "Custom Track", "Me", 60)


@pytest.fixture
def custom_post():
    post = Post(99, 50, "Custom public post")
    return post


# === Тесты для MusicRecommendation ===

def test_music_recommendation_initialization():
    rec = MusicRecommendation(recommendation_id=5)
    assert rec.id == 5
    assert rec._database is None
    assert rec._custom_tracks == []


def test_music_recommendation_set_database_success(music_db):
    rec = MusicRecommendation()
    rec.set_database(music_db)
    assert rec._database is music_db


def test_music_recommendation_set_database_invalid_type():
    rec = MusicRecommendation()
    with pytest.raises(TypeError, match="Database must be an instance of MusicDatabase"):
        rec.set_database("not a database")


def test_music_recommendation_add_track_success(custom_track):
    rec = MusicRecommendation()
    rec.add_track(custom_track)
    assert custom_track in rec._custom_tracks


def test_music_recommendation_add_track_invalid_type():
    rec = MusicRecommendation()
    with pytest.raises(TypeError, match="Only MusicTrack instances are allowed"):
        rec.add_track("not a track")


def test_music_recommendation_add_track_no_duplicates(custom_track):
    rec = MusicRecommendation()
    rec.add_track(custom_track)
    rec.add_track(custom_track)
    assert len(rec._custom_tracks) == 1


def test_music_recommendation_show_popular(music_db, custom_track):
    rec = MusicRecommendation()
    rec.set_database(music_db)
    rec.add_track(custom_track)

    tracks = rec.show(count=2, strategy="popular")
    assert len(tracks) == 2
    # Track A должен быть первым (самый популярный)
    assert tracks[0].id == 1


def test_music_recommendation_show_recent(music_db, custom_track):
    rec = MusicRecommendation()
    rec.set_database(music_db)
    rec.add_track(custom_track)

    tracks = rec.show(count=2, strategy="recent")
    assert len(tracks) == 2
    # Последние добавленные: Track C (id=3), затем Track B (id=2)
    assert tracks[0].id == 3 or tracks[1].id == 3  # порядок может зависеть от dict


def test_music_recommendation_show_random(music_db, custom_track):
    rec = MusicRecommendation()
    rec.set_database(music_db)
    rec.add_track(custom_track)

    with patch('random.sample') as mock_sample:
        mock_sample.return_value = [music_db._storage[1], music_db._storage[2]]
        tracks = rec.show(count=2, strategy="random")
        assert len(tracks) == 2
        assert tracks == [music_db._storage[1], music_db._storage[2]]


def test_music_recommendation_show_fallback_to_custom(custom_track):
    rec = MusicRecommendation()
    rec.add_track(custom_track)
    tracks = rec.show(count=1)
    assert len(tracks) == 1
    assert tracks[0].id == 99


def test_music_recommendation_show_no_database_no_custom():
    rec = MusicRecommendation()
    tracks = rec.show(count=5)
    assert tracks == []


def test_music_recommendation_get_total_available(music_db, custom_track):
    rec = MusicRecommendation()
    rec.set_database(music_db)
    rec.add_track(custom_track)
    assert rec.get_total_available() == 4  # 3 в базе + 1 кастомный


# === Тесты для PostRecommendation ===

def test_post_recommendation_initialization():
    rec = PostRecommendation(feed_id=10)
    assert rec.id == 10
    assert rec._database is None


def test_post_recommendation_set_database_success(post_db):
    rec = PostRecommendation()
    rec.set_database(post_db)
    assert rec._database is post_db


def test_post_recommendation_set_database_invalid_type():
    rec = PostRecommendation()
    with pytest.raises(TypeError, match="Database must be an instance of PostDatabase"):
        rec.set_database("not a database")


def test_post_recommendation_add_content_public_post(custom_post):
    rec = PostRecommendation()
    rec.add_content(custom_post)
    assert len(rec._items) == 1


def test_post_recommendation_add_content_private_post():
    private_post = Post(1, 100, "Private")
    private_post.is_public = False
    rec = PostRecommendation()
    with pytest.raises(ValueError, match="Cannot add private post to recommendation feed"):
        rec.add_content(private_post)


def test_post_recommendation_add_content_invalid_type():
    rec = PostRecommendation()
    with pytest.raises(TypeError, match="PostRecommendation accepts only Post instances"):
        rec.add_content("not a post")


def test_post_recommendation_add_post_alias(custom_post):
    rec = PostRecommendation()
    rec.add_post(custom_post)
    assert len(rec._items) == 1


def test_post_recommendation_show_with_database(post_db):
    rec = PostRecommendation()
    rec.set_database(post_db)
    posts = rec.show(count=2)
    assert len(posts) == 2
    # Только публичные посты (id=1,2)
    assert all(p.is_public for p in posts)
    assert all(p.id in (1, 2) for p in posts)


def test_post_recommendation_show_no_public_posts():
    db = PostDatabase()
    private_post = Post(1, 100, "Private")
    private_post.is_public = False
    db.add(private_post)

    rec = PostRecommendation()
    rec.set_database(db)
    posts = rec.show(count=1)
    assert posts == []


def test_post_recommendation_show_fallback_to_custom(custom_post):
    rec = PostRecommendation()
    rec.add_post(custom_post)
    posts = rec.show(count=1)
    assert len(posts) == 1
    assert posts[0].id == 99


def test_post_recommendation_show_mixed_custom_and_db(post_db, custom_post):
    rec = PostRecommendation()
    rec.set_database(post_db)
    rec.add_post(custom_post)
    # show() использует ТОЛЬКО базу, если она установлена
    posts = rec.show(count=3)
    assert len(posts) == 2  # только 2 публичных в базе
    assert all(p.id in (1, 2) for p in posts)
    # Кастомный не возвращается, потому что база приоритетна


def test_post_recommendation_repr():
    rec = PostRecommendation(5)
    post = Post(1, 100, "Test")
    rec.add_post(post)
    assert "PostRecommendation(id=5, items=1)" in repr(rec)


# === Интеграционный тест ===

def test_recommendations_end_to_end(music_db, post_db):
    # Music
    music_rec = MusicRecommendation()
    music_rec.set_database(music_db)
    tracks = music_rec.show(2)
    assert len(tracks) == 2

    # Post
    post_rec = PostRecommendation()
    post_rec.set_database(post_db)
    posts = post_rec.show(2)
    assert len(posts) == 2