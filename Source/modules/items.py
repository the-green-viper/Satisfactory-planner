
class item:
    def __init__(self, name: str, points: int):
        self.name = name # string
        self.points = int(points) # int 
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_points(self):
        return self.points 
    
def item_decoder(dct):
    return item(dct['name'], dct['power'])