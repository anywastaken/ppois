import json
from Investment import Investment
from Exception import IncorrectDataInFileException


class InvestmentDatabase:
    def __init__(self):
        self.database = {}

        try:
            with open("Database/investment.json", "r", encoding="utf-8") as f:
                first_char = f.read(1)
                if first_char != "{":
                    raise IncorrectDataInFileException
                f.seek(0)
                self.database = json.load(f)
        except FileNotFoundError:
            self.save_changes()

    def __repr__(self):
        temp = f""
        for i in self.database:
            temp += f"{i}: {self.database[i][0]},{self.database[i][1]}\n"
        return temp

    def save_changes(self):
        with open("Database/investment.json", "w", encoding="utf-8") as f:
            json.dump(self.database, f, indent=4, ensure_ascii=False)

    def add_investment(self, investment:Investment):
        self.database[investment.name] = [0,investment.percent]
        self.save_changes()

    def delete_investment(self, name):
        if name in self.database:
            del self.database[name]
            self.save_changes()
        else:
            print("Object not found.\n")

    def deposit(self, name:str, amount:int):
        self.database[name][0] +=amount
        self.save_changes()

    def withdraw(self, name:str, amount:int)->int:
        if amount<self.database[name][0]:
            self.database[name][0] -= amount
            self.save_changes()
            return 1
        else:
            print("Not enough money.\n")
            return 0