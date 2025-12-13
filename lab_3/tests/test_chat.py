import pytest
from datetime import datetime
from social_network.chat.Chat import Chat
from social_network.chat.Message import Message
from social_network.chat.GroupChat import GroupChat
from social_network.chat.PrivateChat import PrivateChat
from social_network.exceptions.InsufficientPermissionsException import InsufficientPermissionsException





# Подкласс для тестирования абстрактного класса Chat
class ConcreteChat(Chat):
    pass


@pytest.fixture
def sample_chat():
    """Фикстура для создания экземпляра ConcreteChat."""
    return ConcreteChat(chat_id=99)


def test_chat_initialization(sample_chat):
    """Тест инициализации чата."""
    assert sample_chat.id == 99
    assert sample_chat.get_message_count() == 0
    assert isinstance(sample_chat.created_at, datetime)


def test_chat_invalid_id():
    """Тест инициализации чата с недопустимым ID."""
    with pytest.raises(ValueError, match="Chat ID must be a positive integer"):
        ConcreteChat(chat_id=-1)
    with pytest.raises(ValueError, match="Chat ID must be a positive integer"):
        ConcreteChat(chat_id=0)


def test_send_message_success(sample_chat):
    """Тест успешной отправки сообщения."""
    msg = sample_chat.send_message(sender_id=123, text="Hello!")
    assert msg.sender_id == 123
    assert msg.text == "Hello!"
    assert msg.chat_id == 99
    assert sample_chat.get_message_count() == 1


def test_send_message_empty_text_raises_error(sample_chat):
    """Тест ошибки при попытке отправить пустое сообщение."""
    with pytest.raises(ValueError, match="Message text cannot be empty"):
        sample_chat.send_message(sender_id=123, text="")


def test_send_message_whitespace_only_raises_error(sample_chat):
    """Тест ошибки при отправке сообщения только из пробелов."""
    with pytest.raises(ValueError, match="Message text cannot be empty"):
        sample_chat.send_message(sender_id=123, text="   ")


def test_send_message_invalid_sender_id_raises_error(sample_chat):
    """Тест ошибки при отправке сообщения с недопустимым sender_id."""
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        sample_chat.send_message(sender_id=0, text="Invalid sender")


def test_get_messages_default(sample_chat):
    """Тест получения всех сообщений."""
    sample_chat.send_message(sender_id=1, text="First")
    sample_chat.send_message(sender_id=2, text="Second")
    messages = sample_chat.get_messages()
    assert len(messages) == 2
    assert messages[0].text == "First"
    assert messages[1].text == "Second"


def test_get_messages_with_limit(sample_chat):
    """Тест получения ограниченного количества сообщений."""
    sample_chat.send_message(sender_id=1, text="First")
    sample_chat.send_message(sender_id=2, text="Second")
    sample_chat.send_message(sender_id=3, text="Third")
    messages = sample_chat.get_messages(limit=2)
    assert len(messages) == 2
    assert messages[0].text == "Second"
    assert messages[1].text == "Third"


def test_clear_history(sample_chat):
    """Тест очистки истории сообщений."""
    sample_chat.send_message(sender_id=1, text="To delete")
    assert sample_chat.get_message_count() == 1
    sample_chat.clear_history(user_id=123)  # любой пользователь может вызвать
    assert sample_chat.get_message_count() == 0


def test_find_message_by_id_found(sample_chat):
    """Тест поиска существующего сообщения по ID."""
    sent_msg = sample_chat.send_message(sender_id=1, text="Find me")
    found_msg = sample_chat.find_message_by_id(sent_msg.id)
    assert found_msg is not None
    assert found_msg.id == sent_msg.id
    assert found_msg.text == "Find me"


def test_find_message_by_id_not_found(sample_chat):
    """Тест поиска несуществующего сообщения по ID."""
    sample_chat.send_message(sender_id=1, text="Exists")
    found_msg = sample_chat.find_message_by_id(999)
    assert found_msg is None


def test_repr(sample_chat):
    """Тест строкового представления чата."""
    repr_str = repr(sample_chat)
    assert "ConcreteChat(id=99, messages=0)" in repr_str


# --- Тесты для Message ---

@pytest.fixture
def sample_message():
    """Фикстура для создания экземпляра Message."""
    return Message(message_id=1, chat_id=99, sender_id=123, text="Test message")


def test_message_initialization(sample_message):
    """Тест инициализации сообщения."""
    assert sample_message.id == 1
    assert sample_message.chat_id == 99
    assert sample_message.sender_id == 123
    assert sample_message.text == "Test message"
    assert not sample_message.is_edited


def test_message_invalid_ids_raise_error():
    """Тест ошибки при недопустимых ID."""
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Message(message_id=0, chat_id=99, sender_id=123, text="Invalid message_id")
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Message(message_id=1, chat_id=0, sender_id=123, text="Invalid chat_id")
    with pytest.raises(ValueError, match="IDs must be positive integers"):
        Message(message_id=1, chat_id=99, sender_id=0, text="Invalid sender_id")


def test_message_invalid_text_raise_error():
    """Тест ошибки при пустом тексте сообщения."""
    with pytest.raises(ValueError, match="Message text cannot be empty"):
        Message(message_id=1, chat_id=99, sender_id=123, text="")
    with pytest.raises(ValueError, match="Message text cannot be empty"):
        Message(message_id=1, chat_id=99, sender_id=123, text="  ")


def test_message_text_is_stripped():
    """Тест, что текст сообщения автоматически обрезается."""
    msg = Message(message_id=1, chat_id=99, sender_id=123, text="  Trimmed text  ")
    assert msg.text == "Trimmed text"


def test_message_edit_success(sample_message):
    """Тест успешного редактирования сообщения."""
    sample_message.edit("Updated text")
    assert sample_message.text == "Updated text"
    assert sample_message.is_edited


def test_message_edit_empty_text_raise_error(sample_message):
    """Тест ошибки при попытке отредактировать сообщение в пустой текст."""
    with pytest.raises(ValueError, match="New message text cannot be empty"):
        sample_message.edit("")
    with pytest.raises(ValueError, match="New message text cannot be empty"):
        sample_message.edit("  ")


def test_message_repr(sample_message):
    """Тест строкового представления сообщения."""
    repr_str = repr(sample_message)
    assert "Message(id=1, sender=123, text='Test message...')" in repr_str



@pytest.fixture
def group_chat():
    """Создаёт групповой чат с владельцем 100 и именем 'Test Group'."""
    return GroupChat(chat_id=1, name="Test Group", owner_id=100)


def test_group_chat_initialization():
    """Тест инициализации группового чата."""
    chat = GroupChat(chat_id=5, name="My Team", owner_id=42)
    assert chat.id == 5
    assert chat.name == "My Team"
    assert chat.owner_id == 42
    assert chat.get_participant_count() == 1
    assert chat.get_admin_count() == 1
    assert 42 in chat._participants
    assert 42 in chat._admins


def test_group_chat_invalid_name():
    """Тест ошибки при пустом имени."""
    with pytest.raises(ValueError, match="Chat name cannot be empty"):
        GroupChat(chat_id=1, name="", owner_id=100)
    with pytest.raises(ValueError, match="Chat name cannot be empty"):
        GroupChat(chat_id=1, name="   ", owner_id=100)


def test_group_chat_invalid_owner_id():
    """Тест ошибки при недопустимом owner_id."""
    with pytest.raises(ValueError, match="Owner ID must be positive"):
        GroupChat(chat_id=1, name="Test", owner_id=0)
    with pytest.raises(ValueError, match="Owner ID must be positive"):
        GroupChat(chat_id=1, name="Test", owner_id=-5)


def test_add_participant_success(group_chat):
    """Тест успешного добавления участника."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    assert 200 in group_chat._participants
    assert group_chat.get_participant_count() == 2


def test_add_participant_by_non_admin_fails(group_chat):
    """Тест ошибки при добавлении участника не админом."""
    with pytest.raises(InsufficientPermissionsException, match="User is not an admin"):
        group_chat.add_participant(issuer_id=200, user_id=300)


def test_add_participant_invalid_user_id(group_chat):
    """Тест ошибки при недопустимом user_id."""
    with pytest.raises(ValueError, match="User ID must be positive"):
        group_chat.add_participant(issuer_id=100, user_id=0)


def test_remove_participant_success(group_chat):
    """Тест успешного удаления участника."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    group_chat.remove_participant(issuer_id=100, user_id=200)
    assert 200 not in group_chat._participants
    assert group_chat.get_participant_count() == 1


def test_remove_participant_by_moderator_success(group_chat):
    """Тест удаления обычного участника админом (не владельцем)."""
    # Добавляем двух участников: 200 и 300
    group_chat.add_participant(issuer_id=100, user_id=200)
    group_chat.add_participant(issuer_id=100, user_id=300)
    # Назначаем 200 админом
    group_chat.add_admin(issuer_id=100, user_id=200)
    # Админ 200 удаляет участника 300
    group_chat.remove_participant(issuer_id=200, user_id=300)
    assert 300 not in group_chat._participants
    assert group_chat.get_participant_count() == 2  # владелец + админ

def test_remove_owner_fails(group_chat):
    """Тест ошибки при попытке удалить владельца."""
    with pytest.raises(ValueError, match="Cannot remove chat owner"):
        group_chat.remove_participant(issuer_id=100, user_id=100)


def test_remove_participant_by_non_admin_fails(group_chat):
    """Тест ошибки при удалении не админом."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    with pytest.raises(InsufficientPermissionsException, match="Only admins can remove participants"):
        group_chat.remove_participant(issuer_id=200, user_id=100)


def test_add_admin_success(group_chat):
    """Тест успешного назначения админа."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    group_chat.add_admin(issuer_id=100, user_id=200)
    assert 200 in group_chat._admins
    assert group_chat.get_admin_count() == 2


def test_add_admin_by_non_owner_fails(group_chat):
    """Тест ошибки при назначении админа не владельцем."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    with pytest.raises(InsufficientPermissionsException, match="Only owner can appoint admins"):
        group_chat.add_admin(issuer_id=200, user_id=300)


def test_add_admin_non_participant_fails(group_chat):
    """Тест ошибки при назначении не участника админом."""
    with pytest.raises(ValueError, match="User must be a participant first"):
        group_chat.add_admin(issuer_id=100, user_id=999)


def test_send_message_by_participant_success(group_chat):
    """Тест отправки сообщения участником."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    msg = group_chat.send_message(sender_id=200, text="Hi!")
    assert msg.text == "Hi!"
    assert msg.sender_id == 200
    assert group_chat.get_message_count() == 1


def test_send_message_by_non_participant_fails(group_chat):
    """Тест ошибки при отправке не участником."""
    with pytest.raises(InsufficientPermissionsException, match="User is not a participant"):
        group_chat.send_message(sender_id=999, text="Spam")


def test_clear_history_by_admin_success(group_chat):
    """Тест очистки истории админом."""
    group_chat.send_message(sender_id=100, text="Old msg")
    group_chat.clear_history(user_id=100)
    assert group_chat.get_message_count() == 0


def test_clear_history_by_non_admin_fails(group_chat):
    """Тест ошибки при очистке не админом."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    with pytest.raises(InsufficientPermissionsException, match="Only admins can clear history"):
        group_chat.clear_history(user_id=200)


def test_removed_user_loses_admin_status(group_chat):
    """Тест, что удаление участника убирает его из админов."""
    group_chat.add_participant(issuer_id=100, user_id=200)
    group_chat.add_admin(issuer_id=100, user_id=200)
    assert 200 in group_chat._admins
    group_chat.remove_participant(issuer_id=100, user_id=200)
    assert 200 not in group_chat._admins


@pytest.fixture
def private_chat():
    """Создаёт приватный чат между 101 и 102."""
    return PrivateChat(chat_id=10, user1_id=101, user2_id=102)


def test_private_chat_initialization():
    """Тест инициализации приватного чата."""
    chat = PrivateChat(chat_id=5, user1_id=1, user2_id=2)
    assert chat.id == 5
    assert chat.user1_id == 1
    assert chat.user2_id == 2


def test_private_chat_same_user_fails():
    """Тест ошибки при создании чата с самим собой."""
    with pytest.raises(ValueError, match="Cannot create private chat with yourself"):
        PrivateChat(chat_id=1, user1_id=123, user2_id=123)


def test_private_chat_invalid_user_ids():
    """Тест ошибки при недопустимых ID."""
    with pytest.raises(ValueError, match="User IDs must be positive integers"):
        PrivateChat(chat_id=1, user1_id=0, user2_id=2)
    with pytest.raises(ValueError, match="User IDs must be positive integers"):
        PrivateChat(chat_id=1, user1_id=-1, user2_id=2)


def test_send_message_by_participant_success(private_chat):
    """Тест отправки сообщения участником."""
    msg = private_chat.send_message(sender_id=101, text="Hello")
    assert msg.text == "Hello"
    assert private_chat.get_message_count() == 1


def test_send_message_by_non_participant_fails(private_chat):
    """Тест ошибки при отправке не участником."""
    with pytest.raises(InsufficientPermissionsException, match="User is not a participant"):
        private_chat.send_message(sender_id=999, text="Spam")


def test_get_other_user_id_success(private_chat):
    """Тест получения ID собеседника."""
    assert private_chat.get_other_user_id(101) == 102
    assert private_chat.get_other_user_id(102) == 101


def test_get_other_user_id_non_participant_fails(private_chat):
    """Тест ошибки при запросе собеседника не участником."""
    with pytest.raises(ValueError, match="User is not a participant"):
        private_chat.get_other_user_id(999)


def test_clear_history_by_participant_success(private_chat):
    """Тест очистки истории участником."""
    private_chat.send_message(sender_id=101, text="Old")
    private_chat.clear_history(user_id=102)
    assert private_chat.get_message_count() == 0


def test_clear_history_by_non_participant_fails(private_chat):
    """Тест ошибки при очистке не участником."""
    with pytest.raises(InsufficientPermissionsException, match="User is not a participant"):
        private_chat.clear_history(user_id=999)