import pytest
import os
import json
from Transaction import Transaction
from TransactionHistory import TransactionHistory
from Exception import IncorrectDataInFileException

# Используем ту же логику с временной папкой
@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    db_dir = tmp_path / "Database"
    db_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    return db_dir

## 1. Тесты для Transaction
def test_transaction_init():
    t = Transaction("Alice", "Bob", 100)
    assert t.sender == "Alice"
    assert t.recipient == "Bob"
    assert t.amount == 100
    assert isinstance(t.id, str)
    assert len(t.id) > 0

## 2. Тесты для TransactionHistory
def test_history_init_creates_file():
    history = TransactionHistory()
    assert history.history == {}
    assert os.path.exists("Database/history.json")

def test_history_corrupt_file(setup_db):
    # Создаем битый файл для проверки исключения
    file = setup_db / "history.json"
    file.write_text("invalid")
    
    with pytest.raises(IncorrectDataInFileException):
        TransactionHistory()

def test_add_transaction():
    history = TransactionHistory()
    t = Transaction("Alice", "Bob", 50)
    
    history.add_transaction(t)
    
    assert t.id in history.history
    assert history.history[t.id] == ["Alice", "Bob", 50]
    
    # Проверяем, что изменения реально записались в файл
    with open("Database/history.json", "r") as f:
        data = json.load(f)
        assert t.id in data

def test_history_repr():
    history = TransactionHistory()
    t = Transaction("Alice", "Bob", 50)
    history.add_transaction(t)
    
    output = str(history)
    assert "Transaction id: [sender, recipient, amount]" in output
    assert "Alice" in output
    assert "Bob" in output
    assert "50" in output