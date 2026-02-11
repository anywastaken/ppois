import uuid

from details.Detail import Detail
from machines.Machine import Machine

from manufactoring.FactoryExport import FactoryExport
from manufactoring.InnerStorage import InnerStorage


class ProductionLine:
    def __init__(self):
        self.prod_line_id = uuid.uuid4()
        self.details_list:list[Detail] = []
        self.machine_list:list[Machine] = []
        from manufactoring.Maintenance import Maintenance
        self.maintenance:Maintenance|None = None

    def run_all_machines(self):
        for item in self.machine_list:
            if not item.is_running:
                item.run()

    def stop_all_machines(self):
        for item in self.machine_list:
            if item.is_running:
                item.stop()

    def get_detail(self, detail):
        self.details_list.append(detail)

    def send_all_to_export(self, factory_export:FactoryExport):
        for item in self.details_list:
            factory_export.queue.put(item)
        self.details_list.clear()

    def send_to_export(self, factory_export:FactoryExport, amount):
        for i in range(amount):
            factory_export.queue.put(self.details_list.pop(0))

    def move_all_to_unfinished(self, storage: InnerStorage):
        storage.unfinished_details.extend(self.details_list)
        self.details_list.clear()

    def move_to_unfinished(self, storage: InnerStorage, amount: int):
        count = min(amount, len(self.details_list))
        for _ in range(count):
            storage.unfinished_details.append(self.details_list.pop(0))

    def move_all_to_finished(self, storage: InnerStorage):
        storage.finished_details.extend(self.details_list)
        self.details_list.clear()

    def move_to_finished(self, storage: InnerStorage, amount: int):
        count = min(amount, len(self.details_list))
        for _ in range(count):
            storage.finished_details.append(self.details_list.pop(0))