from staff.Employee import Employee
from staff.Worker import Worker


class Manager(Employee):
    def __init__(self, department:str):
        super().__init__()
        self.department = department

    def sign(self, thing):
        thing.sign = self.sign

    def shout_at_worker(self, worker:Worker):
        print('WORK HARDER!!!')
        worker.attentiveness = True
