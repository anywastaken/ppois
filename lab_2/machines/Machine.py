import uuid

from exceptions.MachineAlreadyRunningError import MachineAlreadyRunningError
from exceptions.MachineNotRunningError import MachineNotRunningError
from details.Assembly import Assembly
from details.Blueprint import BluePrint
from details.Detail import Detail


class Machine:
    def __init__(self):
        self.machine_id = uuid.uuid4()
        self.model:str = ''
        self.capacity:int = 0
        self.is_running:bool = False
        self.instruction:BluePrint | Assembly | None = None
        self.defect_chance:float = 0.1

    def run(self):
        if self.is_running:
            raise MachineAlreadyRunningError
        self.is_running = True

    def stop(self):
        if not self.is_running:
            raise MachineNotRunningError
        self.is_running = False

    def make_detail(self)->Detail:
        if not self.is_running:
            raise MachineNotRunningError
        detail = Detail(self.defect_chance)
        if detail.defect:
            self.defect_chance += 0.1
        detail.name = self.instruction.result
        detail.mass = self.instruction.mass
        detail.price = self.instruction.price
        return detail