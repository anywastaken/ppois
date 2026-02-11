from manufactoring.InnerStorage import InnerStorage


class FactoryImport:
    def __init__(self, import_id: str):
        self.import_id = import_id
        self.queue: list = []

    def send_all_materials_to_inner(self, inner_storage:InnerStorage):
        for material in self.queue:
            inner_storage.materials.append(material)

        self.queue.clear()

    def send_n_materials_to_inner(self, inner_storage:InnerStorage, n: int):
        count = min(n, len(self.queue))

        for _ in range(count):
            material = self.queue.pop(0)
            inner_storage.materials.append(material)

        return count