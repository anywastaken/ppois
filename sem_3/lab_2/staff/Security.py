from staff.Employee import Employee
from warehouse.DeliveryTruk import DeliveryTruck


class Security(Employee):
    def __init__(self):
        super().__init__()
        self.attentiveness: bool | None = None


    def check_truck(self, truck:DeliveryTruck):
        if self.attentiveness:
            if truck.contraband:
                self.help(truck)


    def help(self, truck:DeliveryTruck):
        print('YOU SHELL NOT PASS!!!')
        del truck