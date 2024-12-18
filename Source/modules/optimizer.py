import modules.recipes as recipes

def create_opti_variables(optimizer, recipe_path, opti_variables: dict):
    for recipe in recipe_path:
        if isinstance(recipe, recipes.recipe):
            opti_variables[recipe.get_name()] = optimizer.variable(1,1)
        else :
            create_opti_variables(optimizer, recipe, opti_variables)
    
def create_opti_parameters(optimizer, opti_variables, opti_parameters: dict, 
recipes_dict: dict):
    # Parameters signal the amount of surplus that needs to be produced, a negative value means that there is an external income of that item

    for recipe_name in opti_variables:
        recipe = recipes_dict[recipe_name]

        for input in recipe.get_inputs():
            try :
                opti_parameters[input[0].get_class_name()]
            except KeyError:
                opti_parameters[input[0].get_class_name()] = optimizer.parameter(1, 1)
                optimizer.set_value(opti_parameters[input[0].get_class_name()], 0)

        for output in recipe.get_outputs():
            try :
                opti_parameters[output[0].get_class_name()]
            except KeyError:
                opti_parameters[output[0].get_class_name()] = optimizer.parameter(1, 1)
                optimizer.set_value(opti_parameters[output[0].get_class_name()], 0)

def add_balance_constraints(optimizer, opti_variables: dict, opti_parameters: dict, recipe_dict: dict, items_output: dict, items_input: dict):
    
    for recipe_name in opti_variables:
        recipe = recipe_dict[recipe_name]
        inputs = recipe.get_inputs()
        outputs = recipe.get_outputs()

        for input in inputs:
            try:
                items_input[input[0].get_class_name()] += opti_variables[recipe_name] * input[1] * recipe.get_single_machine_output()
            except KeyError:
                items_input[input[0].get_class_name()] = opti_variables[recipe_name] * input[1] * recipe.get_single_machine_output()

        for output in outputs:
            try:
                items_output[output[0].get_class_name()] += opti_variables[recipe_name] * output[1] * recipe.get_single_machine_output()
            except KeyError:
                items_output[output[0].get_class_name()] = opti_variables[recipe_name] * output[1] * recipe.get_single_machine_output()

    for item in opti_parameters:
        try:
            item_output = items_output[item]
        except KeyError:
            item_output = 0

        try:
            item_input = items_input[item]
        except KeyError:
            item_input = 0

        optimizer.subject_to(item_output - item_input >= opti_parameters[item])

def get_sink_points(items_output: dict, items_input: dict, items_dict: dict):
    sink_points =  0

    for item in items_output:
        if items_dict[item].get_sinkable():
            sink_points += items_output[item] * items_dict[item].get_points()

    for item in items_input:
        if items_dict[item].get_sinkable():
            sink_points -= items_input[item] * items_dict[item].get_points()

    return sink_points
    
def get_power_consumption(opti_variables: dict, recipe_dict: dict,):
    power_consumption = 0

    for recipe_name in opti_variables:
        recipe = recipe_dict[recipe_name]
        power_consumption += opti_variables[recipe_name] * recipe.get_machine().get_power()

    return power_consumption     

def print_soltuion( opti_variables: dict, solution ):
    for recipe_name in opti_variables:
        print(recipe_name, ":", round(solution.value(opti_variables[recipe_name]),2))