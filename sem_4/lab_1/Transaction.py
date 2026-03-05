import uuid


class Transaction:
    def __init__(self, sender, recipient, amount):
        self.sender: str = sender
        self.recipient: str = recipient
        self.amount: int = amount
        self.id = str(uuid.uuid4())