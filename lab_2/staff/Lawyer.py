from staff.Employee import Employee
from staff.GeneralManager import GeneralManager
from warehouse.Condition import Condition
from warehouse.Contract import Contract
from warehouse.Supplier import Supplier


class Lawyer(Employee):
    def __init__(self, sphere:str):
        super().__init__()
        self.sphere:str = sphere

    def make_a_contract(self, side_1:GeneralManager, side_2:Supplier, conditions:list[Condition])->Contract:
        contract = Contract(side_1, side_2)
        contract.conditions = conditions
        return contract

    def sign_a_contract(self, contract:Contract):
        contract.lawyers_sign = self.sign