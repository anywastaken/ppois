import pytest
import os
from BankAccount import BankAccount

# Общая фикстура для всех тестов
@pytest.fixture(autouse=True)
def setup_env(tmp_path, monkeypatch):
    db_dir = tmp_path / "Database"
    db_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    return db_dir

## 1. Базовые операции со счетами
def test_create_and_get_balance():
    account = BankAccount()
    account.create_bank_account("Alice")
    assert account.get_balance("Alice") == 0
    
    # Проверка на дубликат
    account.create_bank_account("Alice") # Напечатает "already exists"

def test_deposit_and_withdraw(monkeypatch):
    account = BankAccount()
    account.create_bank_account("Bob")
    account.deposit("Bob", 1000)
    assert account.get_balance("Bob") == 1000

    # Имитируем ввод категории для бюджета при списании
    monkeypatch.setattr('builtins.input', lambda _: "other")
    account.withdraw("Bob", 300)
    assert account.get_balance("Bob") == 700

def test_withdraw_insufficient_funds(capsys, monkeypatch):
    account = BankAccount()
    account.create_bank_account("Bob")
    account.deposit("Bob", 100)
    account.withdraw("Bob", 500)
    
    assert "Not enough money" in capsys.readouterr().out
    assert account.get_balance("Bob") == 100

## 2. Транзакции
def test_transaction_between_accounts():
    account = BankAccount()
    account.create_bank_account("Alice")
    account.create_bank_account("Bob")
    account.deposit("Alice", 500)
    
    account.transaction("Alice", "Bob", 200)
    assert account.get_balance("Alice") == 300
    assert account.get_balance("Bob") == 200

## 3. Инвестиции и бюджеты (Интеграция)
def test_transaction_out_to_investment(monkeypatch):
    account = BankAccount()
    account.create_bank_account("Alice")
    account.deposit("Alice", 1000)
    
    # Создаем инвестицию через мок ввода
    inputs = iter(["Gold", "10"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    account.add_investment()
    
    # Переводим в инвестицию
    # Важно: withdraw вызовет detect_operation, которому нужен ввод категории
    monkeypatch.setattr('builtins.input', lambda _: "other")
    account.transaction_out("Alice", "Gold", 400)
    
    assert account.get_balance("Alice") == 600
    assert account.investments.database["Gold"][0] == 400

def test_transaction_from_investment(monkeypatch):
    account = BankAccount()
    account.create_bank_account("Alice")
    
    # 1. Создаем инвестицию "Crypto" с 5%
    inputs_add = iter(["Crypto", "5"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_add))
    account.add_investment()
    
    # 2. Кладем туда деньги вручную для теста
    account.investments.deposit("Crypto", 500)
    
    # 3. Переводим из инвестиции на счет
    # Нужно 3 ввода: sender, recipient, amount
    inputs_trans = iter(["Crypto", "Alice", "200"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs_trans))
    
    account.transaction_from_investment()
    assert account.get_balance("Alice") == 200
    assert account.investments.database["Crypto"][0] == 300

## 4. Проверка вывода (UI методы)
def test_show_methods(capsys):
    account = BankAccount()
    account.show_transaction_history()
    account.show_budget_database()
    account.show_investment_database()
    
    out = capsys.readouterr().out
    assert "Transaction id" in out
    assert "Name/amount/limit" in out
    assert "Name/amount/percent" in out