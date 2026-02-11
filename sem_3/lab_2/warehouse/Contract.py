import uuid

from staff.GeneralManager import GeneralManager
from warehouse.Condition import Condition
from warehouse.Supplier import Supplier


class Contract:
    def __init__(self, general_manager:GeneralManager, supplier:Supplier):
        self.contract_id = uuid.uuid4()
        self.side_factory = general_manager
        self.side_supplier = supplier
        self.conditions:list[Condition] = []
        self.side_factory_sign = None
        self.side_supplier_sign = None
        self.lawyers_sign = None