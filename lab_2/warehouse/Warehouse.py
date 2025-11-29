from staff.Security import Security
from warehouse.DeliveryTruk import DeliveryTruck
from warehouse.DetailStorageCell import DetailStorageCell
from warehouse.MaterialStorageCell import MaterialStorageCell
from warehouse.WarehouseExport import WarehouseExport
from warehouse.WarehouseImport import WarehouseImport


class Warehouse:
    def __init__(self, delivery_truck:DeliveryTruck, materials:MaterialStorageCell, details:DetailStorageCell,
                 address:str, security:list[Security]):
        self.delivery_truck:DeliveryTruck|None = delivery_truck
        self.materials:MaterialStorageCell|None = materials
        self.details:DetailStorageCell|None = details
        self.address:str = address
        self.security:list[Security] = security
        self.export_for_sale:WarehouseExport = WarehouseExport('export')
        self.export_to_factory:WarehouseExport = WarehouseExport('factory')
        self.import_from_factory:WarehouseImport = WarehouseImport('factory')
        self.import_from_supplier:WarehouseImport = WarehouseImport('supplier')