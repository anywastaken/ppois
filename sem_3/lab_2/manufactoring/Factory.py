from manufactoring.Workshop import Workshop
from manufactoring.FactoryExport import FactoryExport
from manufactoring.FactoryImport import FactoryImport
from manufactoring.InnerStorage import InnerStorage


class Factory:
    def __init__(self):
        self.name:str = ''
        self.address:str = ''
        self.workshop_list:list[Workshop] = []
        self.factory_export:FactoryExport | None = None
        self.factory_import:FactoryImport | None = None
        self.inner_storage:InnerStorage | None = None