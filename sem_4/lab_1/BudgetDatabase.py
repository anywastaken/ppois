import json
from Budget import Budget
from Exception import IncorrectDataInFileException

class BudgetDatabase:
    def __init__(self):
        self.database = {}

        try:
            with open("Database/budget.json", "r", encoding="utf-8") as f:
                first_char = f.read(1)
                if first_char != "{":
                    raise IncorrectDataInFileException
                f.seek(0)
                self.database = json.load(f)
        except FileNotFoundError:
            budget = Budget("other", 0)
            self.add_budget(budget)
            self.save_changes()

    def __repr__(self):
        temp = f""
        for i in self.database:
            temp += f"{i}: {self.database[i][0]},{self.database[i][1]}\n"
        return temp

    def add_budget(self, budget:Budget):
        self.database[budget.category] = [0,budget.limit]
        self.save_changes()

    def save_changes(self):
        with open("Database/budget.json", "w", encoding="utf-8") as f:
            json.dump(self.database, f, indent=4, ensure_ascii=False)

    def detect_operation(self, amount:int):
        category = str(input("Input category:"))
        if category in self.database:
            self.database[category][0]+=amount
            if self.database[category][0]>self.database[category][1]:
                print(f"Budget \"{category}\" is overflowing!")
        else:
            self.database["other"][0]+=amount
            if self.database["other"][0] > self.database["other"][1]:
                print(f"Budget \"other\" is overflowing!")
        self.save_changes()

    def delete_budget(self, category:str):
        if category == "other":
            print("This category can't be deleted.")
        elif category in self.database:
            del self.database[category]
            self.save_changes()
        else:
            print("Object not found.\n")

    def reset_budget(self, category:str):
        if category in self.database:
            self.database[category][0] = 0
            self.save_changes()
        else:
            print("Object not found.\n")

    def change_limit(self, category):
        if category in self.database:
            new_limit = int(input("Input new limit:"))
            self.database[category][1] = new_limit
            self.save_changes()
        else:
            print("Object not found.\n")