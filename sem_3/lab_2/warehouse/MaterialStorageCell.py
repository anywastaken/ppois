from materials.Material import Material
from exceptions.StorageOverflowError import StorageOverflowError
from exceptions.InsufficientMaterialsError import InsufficientMaterialsError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from warehouse.WarehouseExport import WarehouseExport

class MaterialStorageCell:
    def __init__(self, storage_cell_id:str, size:int):
        self.storage: list[Material] = []
        self.storage_cell_id = storage_cell_id
        self.size = size

    def append(self, item):
        if len(self.storage) >= self.size:
            raise StorageOverflowError(f"Storage '{self.storage_cell_id}' can contain only {self.size} items")
        self.storage.append(item)

    def send_to_export(self, warehouse_export: "WarehouseExport", amount: int):
        if amount > len(self.storage):
            raise InsufficientMaterialsError(
                f"Requested {amount} items but storage '{self.storage_cell_id}' contains only {len(self.storage)}"
            )

        for _ in range(amount):
            warehouse_export.queue.put(self.storage.pop(0))

    def send_all_to_export(self, warehouse_export: "WarehouseExport"):
        while self.storage:
            warehouse_export.queue.put(self.storage.pop(0))