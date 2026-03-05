import pytest
import json
import os
from Budget import Budget
from BudgetDatabase import BudgetDatabase
from Exception import IncorrectDataInFileException

# Фикстура для подготовки временной папки Database
@pytest.fixture(autouse=True)
def setup_database_dir(tmp_path, monkeypatch):
    # Создаем временную директорию 'Database'
    db_dir = tmp_path / "Database"
    db_dir.mkdir()
    # Заставляем код думать, что текущая рабочая директория - это наш tmp_path
    monkeypatch.chdir(tmp_path)
    return db_dir

## 1. Тесты для Budget
def test_budget_init():
    b = Budget("Food", 1000)
    assert b.category == "Food"
    assert b.limit == 1000
    assert b.amount == 0

## 2. Тесты для Exception
def test_exception_raise():
    with pytest.raises(IncorrectDataInFileException):
        raise IncorrectDataInFileException

## 3. Тесты для BudgetDatabase
def test_db_init_creates_default_file():
    # Проверяем, что если файла нет, создается 'other'
    db = BudgetDatabase()
    assert "other" in db.database
    assert os.path.exists("Database/budget.json")

def test_db_init_corrupt_file(setup_database_dir):
    # Создаем битый файл (не начинается с {)
    file = setup_database_dir / "budget.json"
    file.write_text("not a json")
    
    with pytest.raises(IncorrectDataInFileException):
        BudgetDatabase()

def test_add_and_repr():
    db = BudgetDatabase()
    b = Budget("Travel", 500)
    db.add_budget(b)
    assert "Travel" in db.database
    # Проверка __repr__
    output = str(db)
    assert "Travel: 0,500" in output

def test_detect_operation_exists(monkeypatch):
    db = BudgetDatabase()
    db.add_budget(Budget("Rent", 1000))
    # Имитируем ввод категории "Rent"
    monkeypatch.setattr('builtins.input', lambda _: "Rent")
    
    db.detect_operation(500)
    assert db.database["Rent"][0] == 500

def test_detect_operation_other(monkeypatch):
    db = BudgetDatabase()
    # Имитируем ввод категории, которой нет
    monkeypatch.setattr('builtins.input', lambda _: "Unknown")
    
    db.detect_operation(100)
    assert db.database["other"][0] == 100

def test_delete_budget():
    db = BudgetDatabase()
    db.add_budget(Budget("Gym", 200))
    
    # Удаление существующего
    db.delete_budget("Gym")
    assert "Gym" not in db.database
    
    # Попытка удалить 'other'
    db.delete_budget("other") # Должно просто напечатать текст
    assert "other" in db.database

def test_reset_budget():
    db = BudgetDatabase()
    db.add_budget(Budget("Taxi", 300))
    db.database["Taxi"][0] = 150 # тратим деньги вручную для теста
    
    db.reset_budget("Taxi")
    assert db.database["Taxi"][0] == 0

def test_change_limit(monkeypatch):
    db = BudgetDatabase()
    db.add_budget(Budget("Books", 100))
    
    # Имитируем ввод нового лимита "500"
    monkeypatch.setattr('builtins.input', lambda _: "500")
    db.change_limit("Books")
    assert db.database["Books"][1] == 500

def test_not_found_scenarios(capsys):
    db = BudgetDatabase()
    # Проверяем ветки, где объект не найден
    db.delete_budget("NonExistent")
    db.reset_budget("NonExistent")
    db.change_limit("NonExistent")
    
    captured = capsys.readouterr()
    assert "Object not found" in captured.out