from machines.AssemblyMachine import AssemblyMachine
from exceptions.MachineAlreadyRunningError import MachineAlreadyRunningError
from exceptions.MachineNotRunningError import MachineNotRunningError
from details.Wheel import Wheel
from details.Disk import Disk
from details.Tire import Tire
from details.Assembly import Assembly

class WheelAssemblyMachine(AssemblyMachine):
    def __init__(self):
        super().__init__()
        self.instruction:Assembly | None = None

    def run(self):
        if self.is_running:
            raise MachineAlreadyRunningError
        self.is_running = True

    def stop(self):
        if not self.is_running:
            raise MachineNotRunningError
        self.is_running = False

    def assembly_detail(self, disk:Disk, tire:Tire)->Wheel:
        if not self.is_running:
            raise MachineNotRunningError
        detail = Wheel(self.defect_chance)
        if detail.defect:
            self.defect_chance += 0.1
        detail.name = self.instruction.result
        detail.mass = self.instruction.mass
        detail.price = self.instruction.price
        detail.components.append(disk)
        detail.components.append(tire)
        return detail