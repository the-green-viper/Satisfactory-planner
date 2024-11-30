import json

class machine:
    def __init__(self, name: str, power: float):
        self.name = name
        self.power = power
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_power(self):
        return self.power
    
def machine_decoder(dct):
    return machine(dct['name'], dct['power'])