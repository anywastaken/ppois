import pytest

from details.Assembly import Assembly
from details.Blueprint import BluePrint
from exceptions.ExportDirectionError import ExportDirectionError
from exceptions.ImportDirectionError import ImportDirectionError
from manufactoring.Factory import Factory
from manufactoring.InnerStorage import InnerStorage
from manufactoring.ProductionLine import ProductionLine
from manufactoring.Workshop import Workshop
from materials.CastIron import Steel as CastIronSteel
from materials.Glass import Glass
from materials.StainlessSteel import StainlessSteel
from materials.Wood import Wood
from staff.Accountant import Accountant
from warehouse.WarehouseExport import WarehouseExport
from warehouse.WarehouseImport import WarehouseImport


def test_factory_workshop_and_inner_storage_setup():
    line = ProductionLine()
    workshop = Workshop("w1", "assembly", [line], equipment_list=["press"])
    factory = Factory()
    factory.address = "Industrial Ave"
    factory.workshop_list.append(workshop)

    storage = InnerStorage()

    assert factory.workshop_list[0].equipment_list == ["press"]
    assert storage.unfinished_details == []


def test_instruction_and_material_variants(capsys):
    blueprint = BluePrint()
    assembly = Assembly()
    assert blueprint.components == []
    assert assembly.components == []

    cast_iron = CastIronSteel()
    cast_iron.make_sound()
    cast_iron.rust()

    glass = Glass()
    glass.make_sound()
    glass.make_reflection()

    wood = Wood()
    wood.make_sound()
    wood.contact_with_water()
    assert wood.is_rotten is True

    stainless = StainlessSteel()
    stainless.make_sound()
    stainless.rust()

    output = capsys.readouterr().out
    assert "Stainless steel" in output


def test_accountant_and_export_import_direction_validation():
    accountant = Accountant()
    accountant.issue_salaries()
    accountant.generate_salary_report()

    warehouse_export = WarehouseExport("factory")
    warehouse_export.set_direction("export")
    assert warehouse_export.direction == "export"
    with pytest.raises(ExportDirectionError):
        WarehouseExport("bad")
    with pytest.raises(ExportDirectionError):
        warehouse_export.set_direction("bad")

    importer = WarehouseImport("factory")
    importer.set_direction("export")
    with pytest.raises(ImportDirectionError):
        WarehouseImport("bad")
    with pytest.raises(ImportDirectionError):
        importer.set_direction("bad")
