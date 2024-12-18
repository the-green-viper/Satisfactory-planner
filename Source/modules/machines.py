
class machine:
    def __init__(self, name: str, power: float, class_name: str, variable_power: bool):
        self.name = name
        self.power = power
        self.class_name = class_name
        self.variable_power = variable_power
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_power(self):
        return self.power
    
    def get_class_name(self):
        return self.class_name
    
    def get_variable_power(self):
        return self.variable_power