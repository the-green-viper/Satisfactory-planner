
class machine:
    def __init__(self, name: str, power: float, class_name: str):
        self.name = name
        self.power = power
        self.class_name = class_name
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_power(self):
        return self.power
    
    def get_class_name(self):
        return self.class_name
    
def machine_decoder(dct):
    return machine(dct['name'], dct['power'], dct['class_name'])