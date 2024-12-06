

class recipe:
    def __init__(self, name: str, outputs: tuple, inputs: tuple, single_machine_output: float, machine: str, hard_drive_recipe: bool, active: bool):
        self.name = name # string
        self.outputs = outputs # tuple of tuples (item, amount), item is an item object, amount is a float, amount is per singular main output per minute [#byproduct/(min*#output)] or [1/min]
        self.inputs = inputs # tuple of tuples (item, amount), item is an item object, amount is a float, amount is per singular main output per minute [ #input/(min*#output)]
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

def recipe_decoder_factory(machine_list, items_list, item_recipe_lookup_dict): # the object hook takes a function as an input, this function is called and returns the function that will be used to decode the json
    def recipe_decoder(dct):

        machine = None
        for loaded_machine in machine_list:
            if loaded_machine.get_class_name() == dct['machine']:
                machine = loaded_machine
                break
        if machine is None:
            return None
        
        recipe_name = dct['name']
        recipe_outputs = []
        recipe_inputs = []
        recipe_single_machine_output = dct['single_machine_output']
        recipe_hard_drive_recipe = dct['hard_drive']
        recipe_active = not (recipe_hard_drive_recipe or machine.get_class_name() == 'Build_Converter_C')

        for output in dct['outputs']:
            for item in items_list:
                if item.get_class_name() == output[0]:
                    recipe_outputs.append((item, output[1]))
                    break
        
        for input in dct['inputs']:
            for item in items_list:
                if item.get_class_name() == input[0]:
                    recipe_inputs.append((item, input[1]))
                    break
        
        recipe_object = recipe(
            recipe_name,
            tuple(recipe_outputs),
            tuple(recipe_inputs),
            recipe_single_machine_output,
            machine,
            recipe_hard_drive_recipe,
            recipe_active
        )

        for output in recipe_outputs:
            item_recipe_lookup_dict[output[0].get_class_name()].append(recipe_object)

        return recipe_object
    return recipe_decoder

def calculate_recipe_paths(desired_output, item_recipe_lookup_dict):
    try:
        possible_recipes = item_recipe_lookup_dict[desired_output.get_class_name()]
    except KeyError:
        return []
    
    recipes = []
    
    for possible_recipes_index in range(len(possible_recipes)):
        current_recipe = possible_recipes[possible_recipes_index]
        if current_recipe.get_active(): 
            recipe_chain = [current_recipe.get_name()]
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