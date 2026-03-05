import pytest
import os
import json
from Investment import Investment
from InvestmentDatabase import InvestmentDatabase
from Exception import IncorrectDataInFileException

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    db_dir = tmp_path / "Database"
    db_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    return db_dir

## 1. Тесты для Investment
def test_investment_init_valid():
    inv = Investment("Stocks", 10)
    assert inv.name == "Stocks"
    assert inv.percent == 10

def test_investment_invalid_then_valid(monkeypatch):
    # Имитируем ситуацию: сначала ввели -5 (ошибка), потом 15 (успех)
    inputs = iter(["15"]) 
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    inv = Investment("Crypto", -5) 
    # Сначала сработает print, потом рекурсия возьмет "15" из monkeypatch
    assert inv.percent == 15

## 2. Тесты для InvestmentDatabase
def test_inv_db_init_creates_file():
    db = InvestmentDatabase()
    assert os.path.exists("Database/investment.json")

def test_inv_db_add_and_repr():
    db = InvestmentDatabase()
    inv = Investment("Gold", 5)
    db.add_investment(inv)
    
    assert "Gold" in db.database
    assert "Gold: 0,5" in str(db)

def test_inv_deposit():
    db = InvestmentDatabase()
    db.add_investment(Investment("Bonds", 3))
    
    db.deposit("Bonds", 1000)
    assert db.database["Bonds"][0] == 1000

def test_inv_withdraw_success():
    db = InvestmentDatabase()
    db.add_investment(Investment("Bonds", 3))
    db.deposit("Bonds", 1000)
    
    result = db.withdraw("Bonds", 400)
    assert result == 1
    assert db.database["Bonds"][0] == 600

def test_inv_withdraw_fail(capsys):
    db = InvestmentDatabase()
    db.add_investment(Investment("Bonds", 3))
    db.deposit("Bonds", 100)
    
    result = db.withdraw("Bonds", 500)
    assert result == 0
    assert "Not enough money" in capsys.readouterr().out

def test_inv_delete():
    db = InvestmentDatabase()
    db.add_investment(Investment("Property", 7))
    
    db.delete_investment("Property")
    assert "Property" not in db.database
    
    # Случай, когда не найдено
    db.delete_investment("NonExistent") # Просто печатает текст

def test_inv_db_corrupt(setup_db):
    file = setup_db / "investment.json"
    file.write_text("invalid")
    with pytest.raises(IncorrectDataInFileException):
        InvestmentDatabase()