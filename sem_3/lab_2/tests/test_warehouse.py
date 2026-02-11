import pytest

from details.Detail import Detail
from exceptions.ImportDirectionError import ImportDirectionError
from exceptions.InsufficientDetailsError import InsufficientDetailsError
from exceptions.InsufficientMaterialsError import InsufficientMaterialsError
from exceptions.NoImportModuleError import NoImportModuleError
from exceptions.NotEnoughItemsForTruckError import NotEnoughItemsForTruckError
from exceptions.StorageOverflowError import StorageOverflowError
from exceptions.TruckSizeError import TruckSizeError
from manufactoring.FactoryExport import FactoryExport
from manufactoring.FactoryImport import FactoryImport
from materials.Steel import Steel
from warehouse.DeliveryTruk import DeliveryTruck
from warehouse.DetailStorageCell import DetailStorageCell
from warehouse.MaterialStorageCell import MaterialStorageCell
from warehouse.Warehouse import Warehouse
from warehouse.WarehouseExport import WarehouseExport
from warehouse.WarehouseImport import WarehouseImport


def test_warehouse_import_validation_and_transfer():
    with pytest.raises(ImportDirectionError):
        WarehouseImport("wrong")

    importer = WarehouseImport("factory")
    importer.queue.extend([Steel(), Steel()])

    with pytest.raises(InsufficientMaterialsError):
        importer.send_to_materials([], amount=5)

    with pytest.raises(TypeError):
        importer.queue = [Detail(0.0)]
        importer.send_to_materials([], amount=1)

    importer.queue = [Steel()]
    destination: list[Steel] = []
    importer.send_all_to_materials(destination)
    assert len(destination) == 1

    importer.queue = [Detail(0.0)]
    dest_details: list[Detail] = []
    importer.send_all_to_details(dest_details)
    assert len(dest_details) == 1

    importer.queue = [Steel()]
    with pytest.raises(TypeError):
        importer.send_to_details([], amount=1)


def test_material_and_detail_storage_cells():
    mat_cell = MaterialStorageCell("mat-1", size=1)
    mat_cell.append(Steel())
    with pytest.raises(StorageOverflowError):
        mat_cell.append(Steel())

    export = WarehouseExport("factory")
    mat_cell.send_to_export(export, amount=1)
    assert export.queue.qsize() == 1

    with pytest.raises(InsufficientMaterialsError):
        mat_cell.send_to_export(export, amount=1)

    det_cell = DetailStorageCell("det-1", size=2)
    det_cell.append(Detail(0.0))
    det_cell.append(Detail(0.0))
    with pytest.raises(InsufficientDetailsError):
        det_cell.send_to_export(export, amount=3)

    det_cell.send_all_to_export(export)
    assert export.queue.qsize() == 3


def test_warehouse_export_and_delivery_truck_flow():
    export = WarehouseExport("factory")
    with pytest.raises(NotEnoughItemsForTruckError):
        export.load_truck(DeliveryTruck(), amount=1)

    for _ in range(4):
        export.queue.put(Detail(0.0))

    factory_stub = type("FactoryStub", (), {})()
    factory_stub.factory_import = FactoryImport("import-1")

    export.send_trucks_to_factory(factory_stub, trucks_count=2, load_per_truck=2)
    assert len(factory_stub.factory_import.queue) == 4

    for _ in range(5):
        export.queue.put(Detail(0.0))

    export.send_all_to_export(load_per_truck=3)
    assert export.queue.qsize() == 0


def test_factory_export_to_warehouse_and_truck_validation():
    factory_export = FactoryExport("exp-1")
    truck = DeliveryTruck()
    truck.size = -1
    with pytest.raises(TruckSizeError):
        factory_export.load_truck(truck)

    for _ in range(3):
        factory_export.queue.put(Detail(0.0))

    warehouse = Warehouse(DeliveryTruck(), None, None, "addr", [])
    trucks_sent = factory_export.send_all_to_warehouse(warehouse, truck_size=2)

    assert len(warehouse.import_from_factory.queue) == 3
    assert trucks_sent == 2

    for _ in range(2):
        factory_export.queue.put(Detail(0.0))

    trucks_sent = factory_export.send_n_trucks_to_warehouse(warehouse, truck_size=1, n=5)
    assert trucks_sent == 2


def test_delivery_truck_unloading_paths():
    warehouse = Warehouse(DeliveryTruck(), None, None, "addr", [])
    truck = DeliveryTruck()
    truck.baggage = [Detail(0.0)]

    with pytest.raises(ImportDirectionError):
        truck.unload_to_warehouse(warehouse, "invalid")

    truck.unload_to_warehouse(warehouse, "factory")
    assert warehouse.import_from_factory.queue != []

    truck.baggage = [Detail(0.0)]
    truck.unload_to_warehouse(warehouse, "supplier")
    assert warehouse.import_from_supplier.queue != []

    truck.baggage = [Detail(0.0)]
    factory_stub = type("FactoryStub", (), {"factory_import": None})()
    with pytest.raises(NoImportModuleError):
        truck.unload_to_factory(factory_stub)

    factory_stub.factory_import = FactoryImport("import-1")
    truck.unload_to_factory(factory_stub)
    assert factory_stub.factory_import.queue != []
    assert truck.baggage == []
