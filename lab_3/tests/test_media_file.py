import pytest
from datetime import datetime
from social_network.media.MediaFile import MediaFile


def test_media_file_initialization():
    """Тест успешной инициализации."""
    media = MediaFile(
        media_id=1,
        file_url="https://example.com/photo.jpg",
        media_type="image",
        description="A beautiful photo",
        uploaded_by=100
    )
    assert media.id == 1
    assert media.file_url == "https://example.com/photo.jpg"
    assert media.media_type == "image"
    assert media.description == "A beautiful photo"
    assert media.uploaded_by == 100
    assert isinstance(media.uploaded_at, datetime)
    assert media.is_private is False
    assert media.file_size_bytes is None


def test_media_file_invalid_id():
    """Тест ошибки при недопустимом ID."""
    with pytest.raises(ValueError, match="Media ID must be a positive integer"):
        MediaFile(0, "https://example.com/file.jpg", "image")
    with pytest.raises(ValueError, match="Media ID must be a positive integer"):
        MediaFile(-5, "https://example.com/file.jpg", "image")


def test_media_file_empty_url():
    """Тест ошибки при пустом URL."""
    with pytest.raises(ValueError, match="File URL cannot be empty"):
        MediaFile(1, "", "image")
    with pytest.raises(ValueError, match="File URL cannot be empty"):
        MediaFile(1, "   ", "image")



def test_media_file_valid_urls():
    """Тест допустимых URL."""
    urls = [
        "https://example.com/file.jpg",
        "http://files.site/storage/video.mp4",
        "https://cdn.domain.org/data/document.pdf"
    ]
    for url in urls:
        media = MediaFile(1, url, "document")
        assert media.file_url == url


def test_media_file_unsupported_type():
    """Тест ошибки при неподдерживаемом типе."""
    with pytest.raises(ValueError, match="Unsupported media type"):
        MediaFile(1, "https://example.com/file.jpg", "3d-model")


def test_media_file_supported_types():
    """Тест поддерживаемых типов."""
    for media_type in MediaFile.SUPPORTED_TYPES:
        media = MediaFile(1, "https://example.com/file", media_type)
        assert media.media_type == media_type


def test_media_file_description_stripped():
    """Тест обрезки описания."""
    media = MediaFile(1, "https://example.com/file.jpg", "image", "  description  ")
    assert media.description == "description"


def test_set_file_size_success():
    """Тест установки размера файла."""
    media = MediaFile(1, "https://example.com/file.jpg", "image")
    media.set_file_size(1024)
    assert media.file_size_bytes == 1024


def test_set_file_size_negative_raises_error():
    """Тест ошибки при отрицательном размере."""
    media = MediaFile(1, "https://example.com/file.jpg", "image")
    with pytest.raises(ValueError, match="File size cannot be negative"):
        media.set_file_size(-1)


def test_make_private_and_public():
    """Тест переключения приватности."""
    media = MediaFile(1, "https://example.com/file.jpg", "image")
    assert media.is_private is False
    media.make_private()
    assert media.is_private is True
    media.make_public()
    assert media.is_private is False


def test_get_file_extension():
    """Тест извлечения расширения файла."""
    media1 = MediaFile(1, "https://example.com/photo.JPG", "image")
    assert media1.get_file_extension() == "jpg"

    media2 = MediaFile(1, "https://example.com/video.mp4?expires=123", "video")
    assert media2.get_file_extension() == "mp4"

    media3 = MediaFile(1, "https://example.com/document", "document")
    assert media3.get_file_extension() is None

    media4 = MediaFile(1, "https://example.com/file.tar.gz", "document")
    assert media4.get_file_extension() == "gz"  # только последнее


def test_is_image_and_is_video():
    """Тест методов определения типа."""
    image = MediaFile(1, "https://example.com/photo.jpg", "image")
    video = MediaFile(1, "https://example.com/clip.mp4", "video")
    doc = MediaFile(1, "https://example.com/file.pdf", "document")

    assert image.is_image() is True
    assert image.is_video() is False

    assert video.is_video() is True
    assert video.is_image() is False

    assert doc.is_image() is False
    assert doc.is_video() is False


