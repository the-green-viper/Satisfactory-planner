

class recipe:
    def __init__(self, name: str, outputs: tuple, inputs: tuple, single_machine_output: float, machine: str, hard_drive_recipe: bool, active: bool):
        self.name = name # string
        self.outputs = outputs # tuple of tuples (item, amount), item is an item object, amount is a float, amount is per singular main output [#byproduct/*#output] or 1
        self.inputs = inputs # tuple of tuples (item, amount), item is an item object, amount is a float, amount is per singular main output [ #input/*#output]
        self.single_machine_output = single_machine_output # float, the amount of main output per singular machine per minute [ #output/(min*machine)]
        self.machine = machine # machine object
        self.hard_drive_recipe = hard_drive_recipe # bool
        self.active = active # bool
        
    ### getters
    
    def get_name(self):
        return self.name
    
    def get_outputs(self):
        return self.outputs
    
    def get_inputs(self):
        return self.inputs
    
    def get_single_machine_output(self):
        return self.single_machine_output
    
    def get_machine(self):
        return self.machine
    
    def get_hard_drive_recipe(self):
        return self.hard_drive_recipe

    def get_active(self):
        return self.active
    
    ### other functions
    
    def toggle_active(self):
        self.active = not self.active  # toggle active status

def calculate_recipe_paths(desired_output, item_recipe_lookup_dict: dict):
    try:
        possible_recipes = item_recipe_lookup_dict[desired_output.get_class_name()]
    except KeyError:
        return [] # item is uncraftable
    
    recipes = []
    
    for possible_recipes_index in range(len(possible_recipes)):
        current_recipe = possible_recipes[possible_recipes_index]
        if current_recipe.get_active(): 
            recipe_chain = [current_recipe]
            for input in current_recipe.get_inputs():
                recipe_chain.append(calculate_recipe_paths(input[0], item_recipe_lookup_dict))
            recipes.append(recipe_chain)
    if len(recipes) > 1:
        return tuple(recipes)
    elif len(recipes) == 1:
        return recipes[0]
    else:
        return []
 
# [recipe 0.1, alt recipe 0.1]           
# ([recipe 0.1, [recipe 1.1]], [alt recipe 0.1, [recipe 1.1]])
# ([recipe 0.1, [recipe 1.1, [recipe 2.1, (recipe 2.2, alt recipe 2.2)]]], [alt recipe 0.1, [recipe 1.1]])
# ([recipe 0.1, [recipe 1.1, [recipe 2.1, (recipe 2.2, alt recipe 2.2)]]], [alt recipe 0.1, [recipe 1.1]])