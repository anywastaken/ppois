import pytest
from datetime import datetime
from social_network.content.MusicTrack import MusicTrack


@pytest.fixture
def music_track():
    return MusicTrack(
        track_id=42,
        title="Blinding Lights",
        artist="The Weeknd",
        duration_seconds=203
    )


def test_music_track_initialization(music_track):
    """Тест инициализации трека."""
    assert music_track.id == 42
    assert music_track.title == "Blinding Lights"
    assert music_track.artist == "The Weeknd"
    assert music_track.duration_seconds == 203
    assert music_track.use_count == 0
    assert music_track.is_original_audio is False
    assert music_track.genre is None
    assert isinstance(music_track.created_at, datetime)


def test_music_track_invalid_id():
    """Тест ошибки при недопустимом ID."""
    with pytest.raises(ValueError, match="Track ID must be a positive integer"):
        MusicTrack(0, "Title", "Artist", 180)
    with pytest.raises(ValueError, match="Track ID must be a positive integer"):
        MusicTrack(-5, "Title", "Artist", 180)


def test_music_track_empty_title():
    """Тест ошибки при пустом названии."""
    with pytest.raises(ValueError, match="Track title cannot be empty"):
        MusicTrack(1, "", "Artist", 180)
    with pytest.raises(ValueError, match="Track title cannot be empty"):
        MusicTrack(1, "   ", "Artist", 180)


def test_music_track_empty_artist():
    """Тест ошибки при пустом имени исполнителя."""
    with pytest.raises(ValueError, match="Artist name cannot be empty"):
        MusicTrack(1, "Title", "", 180)
    with pytest.raises(ValueError, match="Artist name cannot be empty"):
        MusicTrack(1, "Title", "   ", 180)


def test_music_track_invalid_duration():
    """Тест ошибки при недопустимой длительности."""
    with pytest.raises(ValueError, match="Duration must be between 1 and 3600 seconds"):
        MusicTrack(1, "Title", "Artist", 0)
    with pytest.raises(ValueError, match="Duration must be between 1 and 3600 seconds"):
        MusicTrack(1, "Title", "Artist", 3601)
    with pytest.raises(ValueError, match="Duration must be between 1 and 3600 seconds"):
        MusicTrack(1, "Title", "Artist", -10)


def test_mark_as_original(music_track):
    """Тест пометки как оригинального звука."""
    music_track.mark_as_original()
    assert music_track.is_original_audio is True


def test_set_genre_success(music_track):
    """Тест установки жанра."""
    music_track.set_genre("Synthwave")
    assert music_track.genre == "Synthwave"


def test_set_genre_empty_raises_error(music_track):
    """Тест ошибки при пустом жанре."""
    with pytest.raises(ValueError, match="Genre cannot be empty"):
        music_track.set_genre("")
    with pytest.raises(ValueError, match="Genre cannot be empty"):
        music_track.set_genre("   ")


def test_increment_use_count(music_track):
    """Тест увеличения счётчика использования."""
    music_track.increment_use_count()
    assert music_track.use_count == 1
    music_track.increment_use_count()
    assert music_track.use_count == 2


def test_get_duration_formatted(music_track):
    """Тест форматирования длительности."""
    assert music_track.get_duration_formatted() == "03:23"

    # Граничные случаи
    short = MusicTrack(2, "Short", "A", 59)
    assert short.get_duration_formatted() == "00:59"

    long = MusicTrack(3, "Long", "B", 3599)
    assert long.get_duration_formatted() == "59:59"


def test_play(capsys, music_track):
    """Тест вывода при воспроизведении (проверка print)."""
    music_track.play()
    captured = capsys.readouterr()
    assert "▶️ Воспроизводится: 'Blinding Lights' — The Weeknd (03:23)" in captured.out


def test_add_to_favorites(capsys, music_track):
    """Тест добавления в избранное."""
    music_track.add_to_favorites(user_id=100)
    captured = capsys.readouterr()
    assert "❤️ Трек 'Blinding Lights' добавлен в избранное пользователем 100" in captured.out


def test_search_by_title_success(music_track):
    """Тест поиска по названию (регистронезависимо)."""
    assert music_track.search_by_title("blinding") is True
    assert music_track.search_by_title("Lights") is True
    assert music_track.search_by_title("BLINDING LIGHTS") is True


def test_search_by_title_not_found(music_track):
    """Тест поиска — не найдено."""
    assert music_track.search_by_title("Starboy") is False
    assert music_track.search_by_title("") is True  # пустой запрос — всегда True (по логике `in`)


def test_repr(music_track):
    """Тест строкового представления."""
    assert repr(music_track) == "MusicTrack(id=42, title='Blinding Lights', artist='The Weeknd')"