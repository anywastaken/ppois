import json

from TransactionHistory import TransactionHistory
from Transaction import Transaction
from BudgetDatabase import BudgetDatabase
from Budget import Budget
from Investment import Investment
from InvestmentDatabase import InvestmentDatabase
from Exception import IncorrectDataInFileException


class BankAccount:
    def __init__(self):
        self.database = {}
        self.history = TransactionHistory()
        self.budgets = BudgetDatabase()
        self.investments = InvestmentDatabase()

        try:
            with open("Database/account.json", "r", encoding="utf-8") as f:
                first_char = f.read(1)
                if first_char!="{":
                    raise IncorrectDataInFileException
                f.seek(0)
                self.database = json.load(f)
        except FileNotFoundError:
            with open("Database/account.json", "w", encoding="utf-8") as f:
                json.dump(self.database, f, ensure_ascii=False, indent=4)

    def __repr__(self):
        temp = f""
        for i in self.database:
            temp += f"{i}: {self.database[i]}\n"
        return temp

    def save_changes(self):
        with open("Database/account.json", "w", encoding="utf-8") as f:
            json.dump(self.database, f, indent=4, ensure_ascii=False)

    def create_bank_account(self, name: str):
        if name not in self.database:
            self.database[name] = 0
            self.save_changes()
        else:
            print("Object already exists.\n")

    def delete_bank_account(self, name: str):
        if name in self.database:
            del self.database[name]
        else:
            print("Object not found.\n")

    def deposit(self, name: str, amount: int):
        if name in self.database:
            self.database[name] += amount
            self.save_changes()
        else:
            print("Object not found.\n")

    def withdraw(self, name: str, amount: int):
        if name in self.database:
            if self.database[name]<amount:
                print("Not enough money.\n")
            else:
                self.database[name] -= amount
                self.save_changes()
                self.budgets.detect_operation(amount)
        else:
            print("Object not found.\n")

    def get_balance(self, name: str) -> int:
        if name in self.database:
            return self.database[name]
        else:
            print("Object not found.\n")
            return 0

    def transaction(self, sender, recipient, amount):
        if sender not in self.database or recipient not in self.database:
            print("Object not found.\n")
        else:
            if self.database[sender]<amount:
                print("Not enough money.\n")
            else:
                self.database[sender]-=amount
                self.deposit(recipient, amount)
                transaction = Transaction(sender, recipient, amount)
                self.history.add_transaction(transaction)

    def transaction_out(self, sender, recipient, amount):
        if sender not in self.database:
            print("Object not found.\n")
        else:
            if self.database[sender]<amount:
                print("Not enough money.\n")
            else:
                if recipient in self.investments.database:
                    self.withdraw(sender, amount)
                    self.investments.deposit(recipient, amount)
                    transaction = Transaction(sender, recipient, amount)
                    self.history.add_transaction(transaction)
                else:
                    self.withdraw(sender, amount)
                    transaction = Transaction(sender, recipient, amount)
                    self.history.add_transaction(transaction)

    def show_transaction_history(self):
        print(self.history)

    def show_budget_database(self):
        print("Name/amount/limit\n")
        print(self.budgets)

    def add_budget(self):
        category = input("Input  category:")
        limit = int(input("Input limit:"))
        budget = Budget(category, limit)
        self.budgets.add_budget(budget)

    def delete_budget(self):
        category = input("input category:")
        self.budgets.delete_budget(category)

    def reset_budget(self):
        category = input("input category:")
        self.budgets.reset_budget(category)

    def change_limit(self):
        category = input("input category:")
        self.budgets.change_limit(category)

    def show_investment_database(self):
        print("Name/amount/percent\n")
        print(self.investments)

    def add_investment(self):
        name = input("Input name:")
        percent = int(input("Input percent:"))
        investment = Investment(name, percent)
        self.investments.add_investment(investment)

    def delete_investment(self):
        name = input("Input name:")
        self.investments.delete_investment(name)

    def transaction_from_investment(self):
        sender = input("Input sender:")
        recipient = input("Input recipient:")
        if sender not in self.investments.database:
            print("Sender not found.\n")
        elif recipient not in self.database:
            print("Recipient not found.\n")
        else:
            amount = int(input("Input amount:"))
            if self.investments.withdraw(sender, amount) == 1:
                self.deposit(recipient, amount)
                transaction = Transaction(sender, recipient, amount)
                self.history.add_transaction(transaction)