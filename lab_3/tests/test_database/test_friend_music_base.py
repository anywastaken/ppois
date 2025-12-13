import pytest
from social_network.database.Database import Database
from social_network.database.FriendDatabase import FriendDatabase
from social_network.database.MusicDatabase import MusicDatabase
from social_network.content.MusicTrack import MusicTrack
from social_network.exceptions.EntityAlreadyExistsException import EntityAlreadyExistsException


# === Тесты для абстрактного Database (через заглушку) ===

class ConcreteEntity:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

class ConcreteDatabase(Database[ConcreteEntity, int]):
    def _get_id(self, entity: ConcreteEntity) -> int:
        return entity.id


@pytest.fixture
def concrete_db():
    return ConcreteDatabase()


def test_database_add(concrete_db):
    entity = ConcreteEntity(1, "Test")
    concrete_db.add(entity)
    assert concrete_db.get_by_id(1) is entity


def test_database_add_duplicate_raises_error(concrete_db):
    entity1 = ConcreteEntity(1, "A")
    entity2 = ConcreteEntity(1, "B")
    concrete_db.add(entity1)
    with pytest.raises(EntityAlreadyExistsException, match="Entity with ID 1 already exists"):
        concrete_db.add(entity2)


def test_database_get_by_id(concrete_db):
    entity = ConcreteEntity(5, "X")
    concrete_db.add(entity)
    assert concrete_db.get_by_id(5) is entity
    assert concrete_db.get_by_id(999) is None


def test_database_get_all(concrete_db):
    e1 = ConcreteEntity(1, "A")
    e2 = ConcreteEntity(2, "B")
    concrete_db.add(e1)
    concrete_db.add(e2)
    all_entities = concrete_db.get_all()
    assert len(all_entities) == 2
    assert e1 in all_entities
    assert e2 in all_entities


def test_database_remove(concrete_db):
    entity = ConcreteEntity(10, "Y")
    concrete_db.add(entity)
    assert concrete_db.remove(10) is True
    assert concrete_db.get_by_id(10) is None
    assert concrete_db.remove(999) is False


def test_database_exists(concrete_db):
    entity = ConcreteEntity(3, "Z")
    concrete_db.add(entity)
    assert concrete_db.exists(3) is True
    assert concrete_db.exists(999) is False


# === Тесты для FriendDatabase ===

@pytest.fixture
def friend_db():
    return FriendDatabase()


def test_friend_database_add_friendship(friend_db):
    friend_db.add_friendship(100, 200)
    assert friend_db.are_friends(100, 200) is True
    assert friend_db.are_friends(200, 100) is True  # симметрия


def test_friend_database_add_duplicate_raises_error(friend_db):
    friend_db.add_friendship(1, 2)
    with pytest.raises(EntityAlreadyExistsException):
        friend_db.add_friendship(1, 2)


def test_friend_database_remove_friendship(friend_db):
    friend_db.add_friendship(1, 2)
    assert friend_db.remove_friendship(1, 2) is True
    assert friend_db.are_friends(1, 2) is False


def test_friend_database_remove_nonexistent(friend_db):
    assert friend_db.remove_friendship(99, 100) is False


def test_get_friends_of(friend_db):
    friend_db.add_friendship(1, 2)
    friend_db.add_friendship(1, 3)
    friend_db.add_friendship(2, 4)
    friends_of_1 = friend_db.get_friends_of(1)
    assert set(friends_of_1) == {2, 3}


def test_get_friend_count(friend_db):
    friend_db.add_friendship(10, 20)
    friend_db.add_friendship(10, 30)
    assert friend_db.get_friend_count(10) == 2


def test_get_mutual_friends(friend_db):
    friend_db.add_friendship(1, 2)
    friend_db.add_friendship(1, 3)
    friend_db.add_friendship(2, 3)
    friend_db.add_friendship(2, 4)
    mutual = friend_db.get_mutual_friends(1, 2)
    assert set(mutual) == {3}


# === Тесты для MusicDatabase ===

@pytest.fixture
def music_db():
    db = MusicDatabase()
    # Добавим тестовые треки
    db.add(MusicTrack(1, "Blinding Lights", "The Weeknd", 203))
    db.add(MusicTrack(2, "Levitating", "Dua Lipa", 205))
    db.add(MusicTrack(3, "Save Your Tears", "The Weeknd", 215))
    db.add(MusicTrack(4, "Original Sound", "User123", 60))
    db._storage[4].mark_as_original()  # помечаем как оригинальный
    db._storage[1].increment_use_count()
    db._storage[1].increment_use_count()  # use_count = 2
    db._storage[2].increment_use_count()  # use_count = 1
    return db


def test_music_database_add_and_get(music_db):
    track = music_db.get_track_by_id(1)
    assert track is not None
    assert track.title == "Blinding Lights"


def test_music_database_search_tracks(music_db):
    results = music_db.search_tracks("weeknd")
    assert len(results) == 2
    assert all("The Weeknd" in t.artist for t in results)


def test_music_database_get_tracks_by_artist(music_db):
    tracks = music_db.get_tracks_by_artist("The Weeknd")
    assert len(tracks) == 2
    assert all(t.artist == "The Weeknd" for t in tracks)


def test_music_database_get_tracks_by_genre(music_db):
    # Установим жанр одному треку
    music_db._storage[1].set_genre("Synthwave")
    tracks = music_db.get_tracks_by_genre("Synthwave")
    assert len(tracks) == 1
    assert tracks[0].title == "Blinding Lights"


def test_music_database_get_original_tracks(music_db):
    originals = music_db.get_original_tracks()
    assert len(originals) == 1
    assert originals[0].title == "Original Sound"


def test_music_database_get_popular_tracks(music_db):
    popular = music_db.get_popular_tracks(limit=2)
    # Blinding Lights (2), Levitating (1)
    assert popular[0].title == "Blinding Lights"
    assert popular[1].title == "Levitating"


def test_music_database_get_recent_tracks(music_db):
    recent = music_db.get_recent_tracks(limit=2)
    # Добавлялись в порядке 1,2,3,4 → последние 2: [3,4] → новые первыми: [4,3]
    assert recent[0].id == 4
    assert recent[1].id == 3


def test_music_database_count_tracks(music_db):
    assert music_db.count_tracks() == 4


def test_music_database_count_tracks_by_artist(music_db):
    assert music_db.count_tracks_by_artist("The Weeknd") == 2


def test_music_database_delete_track(music_db):
    assert music_db.delete_track(2) is True
    assert music_db.get_track_by_id(2) is None
    assert music_db.delete_track(999) is False