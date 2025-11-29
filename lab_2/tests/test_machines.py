import pytest

from details.AssembledDetail import AssembledDetail
from details.Disk import Disk
from details.Tire import Tire
from exceptions.MachineAlreadyRunningError import MachineAlreadyRunningError
from exceptions.MachineNotRunningError import MachineNotRunningError
from machines.AssemblyMachine import AssemblyMachine
from machines.DiskMachine import DiskMachine
from machines.Machine import Machine
from machines.ProductionMachine import ProductionMachine
from machines.TireMachine import TireMachine
from machines.WheelAssemblyMachine import WheelAssemblyMachine


class DummyInstruction:
    def __init__(self, result: str = "Result", mass: float = 2.5, price: int = 42):
        self.result = result
        self.mass = mass
        self.price = price


def test_machine_run_stop_and_make_detail_fields():
    machine = Machine()
    machine.instruction = DummyInstruction(result="Base detail", mass=1.2, price=10)

    machine.run()
    detail = machine.make_detail()
    machine.stop()

    assert detail.name == "Base detail"
    assert detail.mass == 1.2
    assert detail.price == 10
    assert machine.is_running is False


def test_machine_run_stop_errors_and_defect_bump():
    machine = Machine()
    machine.instruction = DummyInstruction()

    machine.run()
    with pytest.raises(MachineAlreadyRunningError):
        machine.run()

    machine.stop()
    with pytest.raises(MachineNotRunningError):
        machine.stop()

    machine.defect_chance = 1.0
    machine.instruction = DummyInstruction(result="Defective")
    machine.run()
    detail = machine.make_detail()

    assert detail.defect is True
    assert machine.defect_chance == pytest.approx(1.1)


def test_production_machine_produces_detail():
    machine = ProductionMachine()
    machine.instruction = DummyInstruction(result="Production", mass=3.3, price=15)

    machine.run()
    detail = machine.make_detail()
    machine.stop()

    assert detail.name == "Production"
    assert detail.mass == 3.3
    assert detail.price == 15
    assert detail.defect in (True, False)


def test_disk_and_tire_machines_use_instructions():
    disk_machine = DiskMachine()
    tire_machine = TireMachine()
    disk_machine.instruction = DummyInstruction(result="Disk result", mass=5.0, price=20)
    tire_machine.instruction = DummyInstruction(result="Tire result", mass=2.0, price=8)

    disk_machine.run()
    tire_machine.run()

    disk_detail = disk_machine.make_detail()
    tire_detail = tire_machine.make_detail()

    assert disk_detail.name == "Disk result"
    assert tire_detail.name == "Tire result"
    assert disk_detail.price == 20
    assert tire_detail.price == 8


def test_assembly_machine_and_wheel_assembly_machine():
    assembly_machine = AssemblyMachine()
    wheel_machine = WheelAssemblyMachine()

    assembly_machine.instruction = DummyInstruction(result="Assembly", mass=7.7, price=33)
    wheel_machine.instruction = DummyInstruction(result="Wheel", mass=4.0, price=25)

    assembly_machine.run()
    assembled = assembly_machine.make_detail()
    assert isinstance(assembled, AssembledDetail)
    assert assembled.name == "Assembly"

    wheel_machine.run()
    disk = Disk(defect_chance=0.0)
    tire = Tire(defect_chance=0.0)
    wheel = wheel_machine.assembly_detail(disk, tire)

    assert wheel.name == "Wheel"
    assert wheel.mass == 4.0
    assert wheel.price == 25
    assert wheel.components == [disk, tire]

    wheel_machine.stop()

    with pytest.raises(MachineNotRunningError):
        WheelAssemblyMachine().assembly_detail(disk, tire)
