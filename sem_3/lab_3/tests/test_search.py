import pytest
from social_network.search.FriendSearch import FriendSearch
from social_network.search.MusicSearch import MusicSearch
from social_network.search.PostSearch import PostSearch
from social_network.search.UserSearch import UserSearch
from social_network.search.StorySearch import StorySearch
from social_network.database.FriendDatabase import FriendDatabase
from social_network.database.MusicDatabase import MusicDatabase
from social_network.database.PostDatabase import PostDatabase
from social_network.database.ReelsDatabase import ReelsDatabase
from social_network.database.SubscriptionDatabase import SubscriptionDatabase
from social_network.database.UserDatabase import UserDatabase
from social_network.database.StoryDatabase import StoryDatabase
from social_network.content.MusicTrack import MusicTrack
from social_network.content.Post import Post
from social_network.content.Reels import Reels
from social_network.content.Story import Story
from social_network.user.User import User
from social_network.user.Profile import Profile

@pytest.fixture
def friend_db():
    db = FriendDatabase()
    db.add_friendship(1, 2)
    db.add_friendship(1, 3)
    return db


@pytest.fixture
def music_db():
    db = MusicDatabase()
    db.add(MusicTrack(1, "Blinding Lights", "The Weeknd", 200))
    db.add(MusicTrack(2, "Levitating", "Dua Lipa", 210))
    db._storage[1].set_genre("synthwave")
    return db


@pytest.fixture
def post_db():
    db = PostDatabase()
    db.add(Post(1, 100, "Hello #world!"))
    db.add(Post(2, 101, "Python is great"))
    return db


@pytest.fixture
def reels_db():
    db = ReelsDatabase()
    r1 = Reels(1, 200)
    r1.record_video()
    r1.add_caption("Dance video")
    # MusicTrack -> строка в reels.music_track
    r1.add_music(MusicTrack(1, "Levitating", "Dua Lipa", 210))
    db.add(r1)
    return db


@pytest.fixture
def subscription_db():
    db = SubscriptionDatabase()
    db.subscribe(100, 200, "user")
    db.subscribe(100, 300, "group")
    return db


@pytest.fixture
def user_db():
    db = UserDatabase()
    p1 = Profile(1)
    p1.set_display_name("Alice Cooper")
    p1.set_bio("Rock legend")
    u1 = User(1, "alice", "alice@example.com", "password123")
    u1.profile = p1
    db.add(u1)
    return db


@pytest.fixture
def story_db():
    db = StoryDatabase()
    s1 = Story(1, 300)
    s1.record_video()
    s1.add_caption("Beach day")
    s1.add_location("Maldives")
    db.add(s1)
    return db




def test_friend_search(friend_db):
    search = FriendSearch(friend_db)
    results = search.search("1", limit=5)
    assert len(results) == 2
    assert all(f.contains_user(1) for f in results)

    with pytest.raises(ValueError):
        search.search("abc")


def test_music_search(music_db):
    search = MusicSearch(music_db)
    results = search.search("weeknd", limit=5)
    assert len(results) == 1
    assert results[0].artist == "The Weeknd"

    results2 = search.search("synthwave", limit=5)
    assert len(results2) == 1
    assert results2[0].genre == "synthwave"


def test_post_search(post_db):
    search = PostSearch(post_db)
    results = search.search("hello", limit=5)
    assert len(results) == 1
    assert "hello" in results[0].content.lower()

    results2 = search.search("world", limit=5)
    assert len(results2) == 1

    results3 = search.search("100", limit=5)
    assert len(results3) == 1
    assert results3[0].author_id == 100


def test_user_search(user_db):
    search = UserSearch(user_db)
    results1 = search.search("alice", limit=5)
    assert len(results1) == 1
    assert results1[0].username == "alice"

    results2 = search.search("rock", limit=5)
    assert len(results2) == 1


def test_story_search(story_db):
    search = StorySearch(story_db)
    results1 = search.search("beach", limit=5)
    assert len(results1) == 1

    results2 = search.search("maldives", limit=5)
    assert len(results2) == 1

    results3 = search.search("300", limit=5)
    assert len(results3) == 1
    assert results3[0].author_id == 300


def test_search_by_id(friend_db, music_db, post_db, reels_db, user_db, story_db):
    music_search = MusicSearch(music_db)
    assert music_search.search_by_id(1).id == 1

    post_search = PostSearch(post_db)
    assert post_search.search_by_id(2).id == 2

    user_search = UserSearch(user_db)
    assert user_search.search_by_id(1).id == 1

    story_search = StorySearch(story_db)
    assert story_search.search_by_id(1).id == 1