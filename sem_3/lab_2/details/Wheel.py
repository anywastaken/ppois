from details.AssembledDetail import AssembledDetail
from details.Disk import Disk
from details.Tire import Tire

class Wheel(AssembledDetail):
    def __init__(self, defect_chance):
        super().__init__(defect_chance)
        self.components:list[Disk|Tire] = []
