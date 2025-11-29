from manufactoring.ProductionLine import ProductionLine

class Workshop:
    def __init__(self, workshop_id:str, workshop_type:str,
                 production_line_list:list[ProductionLine], equipment_list:list):
        self.workshop_id = workshop_id
        self.workshop_type = workshop_type
        self.production_line_list = production_line_list
        self.equipment_list = equipment_list