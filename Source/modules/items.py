
class item:
    def __init__(self, name: str, points: int, class_name: str, sinkable: bool, energy: float, form: str):
        self.name = name # string, name of item
        self.points = int(points) # int, resource sink points
        self.class_name = class_name # sting, name in game json files
        self.sinkable = sinkable # bool, if item can be sunk
        self.energy = energy # float, energy value of item
        self.form = form # string, form of item (solid, liquid, gas)
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_points(self):
        return self.points 
    
    def get_class_name(self):
        return self.class_name
    
    def get_sinkable(self):
        return self.sinkable
    
    def get_energy(self):
        return self.energy
    
    def get_form(self):
        return self.form