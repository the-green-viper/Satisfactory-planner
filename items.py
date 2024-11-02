import recipes

class item:
    def __init__(self, name: str, recipe: recipes.recipe):
        self.name = name # string
        self.recipe = recipe # recipe object
    
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_recipe(self):
        return self.recipe # the object itself is returned, not a copy or name
