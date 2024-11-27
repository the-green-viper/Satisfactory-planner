import recipes

class item:
    def __init__(self, name: str, points: int):
        self.name = name # string
        self.points = points # recipe object
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_recipe(self):
        return self.points 