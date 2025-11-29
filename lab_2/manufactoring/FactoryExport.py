from queue import Queue
from exceptions.TruckSizeError import TruckSizeError

from warehouse.DeliveryTruk import DeliveryTruck
from warehouse.Warehouse import Warehouse

class FactoryExport:
    def __init__(self, export_id:str):
        self.export_id = export_id
        self.queue = Queue()

    def load_truck(self, truck: DeliveryTruck):
        if truck.size <= 0:
            raise TruckSizeError("Размер грузовика не установлен или равен 0.")

        while not self.queue.empty() and len(truck.baggage) < truck.size:
            item = self.queue.get()
            truck.baggage.append(item)

        return truck

    def send_all_to_warehouse(self, warehouse: Warehouse, truck_size: int):
        trucks_sent = 0
        import_queue = warehouse.import_from_factory.queue

        while not self.queue.empty():
            # Создаём грузовик
            truck = DeliveryTruck()
            truck.size = truck_size

            # Загружаем грузовик
            self.load_truck(truck)

            # Отправляем содержимое грузовика в warehouse.import_from_factory
            import_queue.extend(truck.baggage)

            trucks_sent += 1

        return trucks_sent

    def send_n_trucks_to_warehouse(self, warehouse: Warehouse, truck_size: int, n: int):
        trucks_sent = 0
        import_queue = warehouse.import_from_factory.queue

        for _ in range(n):
            if self.queue.empty():
                break

            truck = DeliveryTruck()
            truck.size = truck_size

            self.load_truck(truck)

            # Грузовик может быть пустым, если не хватило груза → не отправляем
            if len(truck.baggage) == 0:
                break

            import_queue.extend(truck.baggage)
            trucks_sent += 1

        return trucks_sent