import json
from Exception import IncorrectDataInFileException

class TransactionHistory:
    def __init__(self):
        self.history = {}

        try:
            with open("Database/history.json", "r", encoding="utf-8") as f:
                first_char = f.read(1)
                if first_char != "{":
                    raise IncorrectDataInFileException
                f.seek(0)
                self.history = json.load(f)
        except FileNotFoundError:
            with open("Database/history.json", "w", encoding="utf-8") as f:
                json.dump(self.history, f, ensure_ascii=False, indent=4)

    def __repr__(self):
        temp = f"Transaction id: [sender, recipient, amount]\n"
        for i in self.history:
            temp += str(i) + ": " + str(self.history[i]) + "\n"
        return temp

    def save_changes(self):
        with open("Database/history.json", "w", encoding="utf-8") as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def add_transaction(self, transaction):
        self.history[transaction.id] = [transaction.sender, transaction.recipient, transaction.amount]
        self.save_changes()