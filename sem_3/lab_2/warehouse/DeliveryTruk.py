from exceptions.ImportDirectionError import ImportDirectionError
from exceptions.NoImportModuleError import NoImportModuleError
from details.Detail import Detail
from staff.Driver import Driver



class DeliveryTruck:
    def __init__(self):
        self.driver:Driver|None = None
        self.size:int = 0
        self.number:int = 0
        self.contraband:bool = False
        self.baggage:list[Detail] = []


    def unload_to_warehouse(self, warehouse, direction: str):
        if direction == 'factory':
            target_import = warehouse.import_from_factory
        elif direction == 'supplier':
            target_import = warehouse.import_from_supplier
        else:
            raise ImportDirectionError(direction)

        for item in self.baggage:
            target_import.queue.append(item)

        self.baggage.clear()

    def unload_to_factory(self, factory):
        if factory.factory_import is None:
            raise NoImportModuleError("У фабрики нет import модуля!")

        # Выгружаем в фабричный импорт
        for item in self.baggage:
            factory.factory_import.queue.append(item)

        # Очищаем грузовик
        self.baggage.clear()

    def unload_to_export(self):
        self.baggage.clear()
