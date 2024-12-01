
class recipe:
    def __init__(self, name: str, outputs: tuple, inputs: tuple, single_machine_output: float, machine: str, hard_drive_recipe: bool, active: bool):
        self.name = name # string
        self.outputs = outputs # tuple of tuples (item, amount), item is a string, amount is a float, amount is per singular main output per minute
        self.inputs = inputs # tuple of tuples (item, amount), item is a string, amount is a float, amount is per singular main output per minute
        self.single_machine_output = single_machine_output # float, the amount of main output per singular machine per minute
        self.machine = machine # string
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

def recipe_decoder_factory(machine_list):    
    def recipe_decoder(dct):
        for loaded_machine in machine_list:
            if loaded_machine.get_name() == dct['machine']:
                machine = loaded_machine
        return recipe(dct['name'], dct['outputs'], dct['inputs'], dct['single_machine_output'], machine, dct['harddrive_recipe'], dct['active'])
    return recipe_decoder