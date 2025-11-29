from staff.Employee import Employee


class GeneralManager(Employee):
    def __init__(self):
        super().__init__()
        self.department = 'factory'

    def sign_a_contract(self, contract):
        contract.side_factory_sign = self.sign