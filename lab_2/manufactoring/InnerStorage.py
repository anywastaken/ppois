from details.Detail import Detail
from manufactoring.FactoryExport import FactoryExport
from materials.Material import Material


class InnerStorage:
    def __init__(self):
        self.unfinished_details:list[Detail] = []
        self.materials:list[Material] = []
        self.finished_details:list[Detail] = []

    def send_all_finished_to_export(self, factory_export:FactoryExport):
        for detail in self.finished_details:
            factory_export.queue.put(detail)

        self.finished_details.clear()

    def send_n_finished_to_export(self, factory_export:FactoryExport, n: int):
        count = min(n, len(self.finished_details))

        for _ in range(count):
            detail = self.finished_details.pop(0)
            factory_export.queue.put(detail)

        return count