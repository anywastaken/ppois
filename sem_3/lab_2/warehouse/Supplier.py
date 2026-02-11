import uuid


class Supplier:
    def __init__(self, name:str, reliability:str):
        self.name = name
        self.reliability = reliability
        self.sign = uuid.uuid4()

    def sign_a_contract(self, contract):
        contract.side_supplier_sign = self.sign