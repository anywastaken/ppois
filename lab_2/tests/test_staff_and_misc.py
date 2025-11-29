import pytest

from exceptions.MissingAttributeError import MissingAttributeError
from manufactoring.Maintenance import Maintenance
from machines.Machine import Machine
from materials.Steel import Steel
from materials.Rubber import Rubber
from other.SocialNetwork import SocialNetwork
from staff.Driver import Driver
from staff.Engineer import Engineer
from staff.GeneralManager import GeneralManager
from staff.Lawyer import Lawyer
from staff.Manager import Manager
from staff.Security import Security
from staff.Smm import Smm
from staff.Worker import Worker
from warehouse.Condition import Condition
from warehouse.Contract import Contract
from warehouse.DeliveryTruk import DeliveryTruck
from warehouse.Supplier import Supplier


def test_social_network_popularity_and_missing_attribute(capsys):
    network = SocialNetwork()
    network.name = "Insta"

    with pytest.raises(MissingAttributeError):
        network.make_popular(object())

    class Thing:
        def __init__(self):
            self.name = "Wheel"

    wheel = Thing()
    network.make_popular(wheel)
    network.ruin_reputation(wheel)

    output = capsys.readouterr().out
    assert "Wheel now is popular" in output
    assert "Reputation of Wheel" in output


def test_smm_manager_driver_and_security_behaviors(capsys):
    smm = Smm()
    smm.film_content()
    smm.edit_content()
    smm.post_content()
    assert smm.raw_content is False
    assert smm.edited_content is False

    manager = Manager("factory")
    worker = Worker()
    worker.attentiveness = False
    manager.shout_at_worker(worker)
    assert worker.attentiveness is True

    driver = Driver()
    driver.attentiveness = False
    driver.drive()
    driver.concentrate()
    assert driver.attentiveness is True
    accident_output = capsys.readouterr().out
    assert "accident" in accident_output

    security = Security()
    security.attentiveness = True
    truck = DeliveryTruck()
    truck.contraband = True
    security.check_truck(truck)


def test_engineer_and_material_helpers():
    maintenance = Maintenance()
    engineer = Engineer()
    engineer.maintenance = maintenance

    machine = Machine()
    machine.defect_chance = 0.5
    engineer.chek_machine(machine)
    assert maintenance.broken_machines == [machine]

    engineer.repair_all()
    assert machine.defect_chance == pytest.approx(0.1)

    steel = Steel()
    steel.rust()
    assert steel.is_rusty is True

    rubber = Rubber()
    rubber.stretch()
    assert rubber.is_stretched is True


def test_contract_signing_flow():
    supplier = Supplier("ACME", "reliable")
    general_manager = GeneralManager()
    lawyer = Lawyer("supply")
    conditions = [Condition("wheel", amount=10, price=5)]

    contract: Contract = lawyer.make_a_contract(general_manager, supplier, conditions)
    general_manager.sign_a_contract(contract)
    supplier.sign_a_contract(contract)
    lawyer.sign_a_contract(contract)

    assert contract.side_factory_sign == general_manager.sign
    assert contract.side_supplier_sign == supplier.sign
    assert contract.lawyers_sign == lawyer.sign
    assert contract.conditions == conditions
