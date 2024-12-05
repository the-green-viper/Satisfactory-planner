
class item:
    def __init__(self, name: str, points: int, class_name: str):
        self.name = name # string, name of item
        self.points = int(points) # int, rescource sink points
        self.class_name = class_name # sting, name in game json files
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_points(self):
        return self.points 
    
def item_decoder(dct):
    return item(dct['name'], dct['points'])