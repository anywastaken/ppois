from queue import Queue
import uuid
from exceptions.ExportDirectionError import ExportDirectionError
from exceptions.NotEnoughItemsForTruckError import NotEnoughItemsForTruckError
from warehouse.DeliveryTruk import DeliveryTruck


class WarehouseExport:
    def __init__(self, direction: str):
        if direction != 'factory' and direction != 'export':
            raise ExportDirectionError(direction)
        else:
            self.direction = direction

        self.export_id = uuid.uuid4()
        self.queue = Queue()

    def set_direction(self, direction: str):
        if direction != 'factory' and direction != 'export':
            raise ExportDirectionError(direction)
        else:
            self.direction = direction

    def load_truck(self, truck: DeliveryTruck, amount: int):
        if amount > self.queue.qsize():
            raise NotEnoughItemsForTruckError(
                f"Requested {amount} items, but only {self.queue.qsize()} available"
            )

        for _ in range(amount):
            truck.baggage.append(self.queue.get())

    def send_trucks_to_factory(self, factory, trucks_count: int, load_per_truck: int):
        for _ in range(trucks_count):

            if self.queue.qsize() < load_per_truck:
                raise NotEnoughItemsForTruckError(
                    f"Not enough items to load next truck "
                    f"(need {load_per_truck}, have {self.queue.qsize()})"
                )

            truck = DeliveryTruck()
            self.load_truck(truck, load_per_truck)
            truck.unload_to_factory(factory)

    def send_all_to_factory(self, factory, load_per_truck: int):
        while not self.queue.empty():

            truck = DeliveryTruck()
            # Сколько можно загрузить в этот грузовик?
            amount = min(load_per_truck, self.queue.qsize())

            self.load_truck(truck, amount)
            truck.unload_to_factory(factory)

    def send_trucks_to_export(self, trucks_count: int, load_per_truck: int):
        for _ in range(trucks_count):

            if self.queue.qsize() < load_per_truck:
                raise NotEnoughItemsForTruckError(
                    f"Not enough items to load next truck "
                    f"(need {load_per_truck}, have {self.queue.qsize()})"
                )

            truck = DeliveryTruck()
            self.load_truck(truck, load_per_truck)
            truck.unload_to_export()

    def send_all_to_export(self, load_per_truck: int):
        while not self.queue.empty():

            truck = DeliveryTruck()
            amount = min(load_per_truck, self.queue.qsize())

            self.load_truck(truck, amount)
            truck.unload_to_export()
