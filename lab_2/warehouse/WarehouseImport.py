import uuid

from exceptions.ImportDirectionError import ImportDirectionError
from exceptions.InsufficientMaterialsError import InsufficientMaterialsError
from exceptions.InsufficientDetailsError import InsufficientDetailsError
from materials.Material import Material
from details.Detail import Detail

class WarehouseImport:
    def __init__(self, direction:str):
        if direction!='factory' and direction!='supplier':
            raise ImportDirectionError(direction)
        else:
            self.direction = direction
        self.import_id = uuid.uuid4()
        self.queue:list = []

    def set_direction(self, direction:str):
        if direction!='factory' and direction!='export':
            raise ImportDirectionError(direction)
        else:
            self.direction = direction


    def send_to_materials(self, material_storage, amount: int):
        if amount > len(self.queue):
            raise InsufficientMaterialsError(
                f"Requested {amount} materials but import queue contains only {len(self.queue)}"
            )

        for _ in range(amount):
            item = self.queue.pop(0)
            if not isinstance(item, Material):
                raise TypeError("WarehouseImport contains non-Material item where Material expected")
            material_storage.append(item)

    def send_all_to_materials(self, material_storage):
        while self.queue:
            item = self.queue[0]
            if not isinstance(item, Material):
                raise TypeError("WarehouseImport contains non-Material item where Material expected")
            material_storage.append(self.queue.pop(0))

    def send_to_details(self, detail_storage, amount: int):
        if amount > len(self.queue):
            raise InsufficientDetailsError(
                f"Requested {amount} details but import queue contains only {len(self.queue)}"
            )

        for _ in range(amount):
            item = self.queue.pop(0)
            if not isinstance(item, Detail):
                raise TypeError("WarehouseImport contains non-Detail item where Detail expected")
            detail_storage.append(item)

    def send_all_to_details(self, detail_storage):
        while self.queue:
            item = self.queue[0]
            if not isinstance(item, Detail):
                raise TypeError("WarehouseImport contains non-Detail item where Detail expected")
            detail_storage.append(self.queue.pop(0))