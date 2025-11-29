import pytest

from details.Detail import Detail
from manufactoring.FactoryExport import FactoryExport
from manufactoring.Maintenance import Maintenance
from manufactoring.ProductionLine import ProductionLine
from staff.Worker import Worker
from machines.ProductionMachine import ProductionMachine


class DummyInstruction:
    def __init__(self, result: str = "Result", mass: float = 1.0, price: int = 5):
        self.result = result
        self.mass = mass
        self.price = price


def test_worker_reports_defects_and_sends_details_to_line():
    prod_line = ProductionLine()
    prod_line.maintenance = Maintenance()

    worker = Worker()
    machine = ProductionMachine()
    machine.instruction = DummyInstruction(result="Widget", mass=2.0, price=9)
    machine.defect_chance = 1.0  # guarantee defect to exercise reporting path
    worker.machine = machine
    worker.attentiveness = True
    worker.production_line = prod_line

    machine.run()
    detail = worker.make_detail()
    worker.send_to_storage(detail)

    assert detail in prod_line.details_list
    assert prod_line.maintenance.broken_machines == [machine]
    assert prod_line.maintenance.reports[0].detail_id == detail.detail_id


def test_worker_loses_no_fingers_when_attentive_on_good_detail():
    prod_line = ProductionLine()
    prod_line.maintenance = Maintenance()

    worker = Worker()
    machine = ProductionMachine()
    machine.instruction = DummyInstruction()
    machine.defect_chance = 0.0

    worker.machine = machine
    worker.attentiveness = True
    worker.production_line = prod_line

    machine.run()
    _ = worker.make_detail()

    assert worker.fingers == 10
    assert prod_line.maintenance.reports == []


def test_production_line_exports_details():
    prod_line = ProductionLine()
    factory_export = FactoryExport("export-1")

    prod_line.details_list = [Detail(0.0) for _ in range(3)]
    prod_line.send_to_export(factory_export, amount=2)
    assert factory_export.queue.qsize() == 2
    assert len(prod_line.details_list) == 1

    prod_line.send_all_to_export(factory_export)
    assert factory_export.queue.qsize() == 3
    assert prod_line.details_list == []


def test_maintenance_repair_resets_defect_chance():
    machine = ProductionMachine()
    machine.defect_chance = 0.7
    maintenance = Maintenance()
    maintenance.add(machine)

    maintenance.repair_all()

    assert machine.defect_chance == pytest.approx(0.1)
