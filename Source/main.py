"""
A planner tool for satisfactory, because the online planners are too limiting.
"""
import json
import os
import re
import casadi

# custom modules
import modules.recipes as recipes
import modules.items as items
import modules.machines as machines
import modules.optimizer as optimizer


def parse_recipe(recipes_raw: list, machines_dict: dict, items_dict: dict, recipes_dict: dict, item_recipe_lookup_dict: dict):
    for recipe_dict_full in recipes_raw:

        recipe_name = recipe_dict_full['mDisplayName']
        recipe_input = recipe_dict_full['mIngredients']
        recipe_output = recipe_dict_full['mProduct']
        recipe_duration = float(recipe_dict_full['mManufactoringDuration'])
        recipe_machine = recipe_dict_full['mProducedIn']
        hard_drive_recipe = 'Alternate' in recipe_name

        recipe_machine_list = recipe_machine.split(',')
        for machine_name_raw in recipe_machine_list:

            if (not "Build_" in machine_name_raw) or ('Build_AutomatedWorkBench_C' in machine_name_raw ):
                continue # skip every recipe that isn't made in a machine
            recipe_machine_class_name = str.join('_C',machine_name_raw.split('.')[-1].split('_C')[0:-1]) + '_C'
            machine = machines_dict[recipe_machine_class_name]

            cycles_per_minute = 60/recipe_duration
                
            recipe_output_items_list = []
            recipe_output_items = recipe_output.split(',')
            for i in range(len(recipe_output_items)//2):    
                item_class_name = str.join('_C',recipe_output_items[i*2].split('.')[-1].split('_C')[0:-1]) + '_C'
                item = items_dict[item_class_name]

                if i == 0:
                    item_amount_per_minute_per_output = 1.0 # is always one because i want to calculate how many input is required to create 1/min of output
                    main_output_amount_string = recipe_output_items[i*2 + 1].split('=')[-1]
                    amount_per_cycle_per_machine_main = float(re.sub("[^0-9\.]", "", main_output_amount_string))
                    recipe_output_items_list.append((item,item_amount_per_minute_per_output))
                else:
                    item_amount_string = recipe_output_items[i*2 + 1].split('=')[-1]
                    item_amount_per_output =  float(re.sub("[^0-9\.]", "", item_amount_string))  / amount_per_cycle_per_machine_main
                    recipe_output_items_list.append((item,item_amount_per_output))


            amount_per_minute_per_machine_main = amount_per_cycle_per_machine_main * cycles_per_minute # to calculate the amount of machines needed for a certain amount of main output [items / (minute*machine)]  

            recipe_input_items_list = []
            recipe_input_items = recipe_input.split(',')
            for i in range(len(recipe_input_items)//2):
                item_class_name = str.join('_C',recipe_input_items[i*2].split('.')[-1].split('_C')[0:-1]) + '_C'
                item = items_dict[item_class_name]

                item_amount_string = recipe_input_items[i*2 + 1].split('=')[-1]
                item_amount_per_output = float(re.sub("[^0-9\.]", "", item_amount_string)) / amount_per_cycle_per_machine_main
                recipe_input_items_list.append((item,item_amount_per_output))

            recipe_output_tuple = tuple(recipe_output_items_list)
            recipe_input_tuple = tuple(recipe_input_items_list)
            recipe_active = not (hard_drive_recipe or machine.get_class_name() == 'Build_Converter_C' or 'Unpackage' in recipe_name)

            recipe = recipes.recipe(recipe_name, 
            recipe_output_tuple, 
            recipe_input_tuple, 
            amount_per_minute_per_machine_main, 
            machine, 
            hard_drive_recipe, 
            recipe_active)

            recipes_dict[recipe_name] = recipe
            for output_tuple in recipe_output_tuple:
                resource_class_name = output_tuple[0].get_class_name()
                resource_recipe = recipe
                if resource_class_name == 'Desc_Water_C' and len(recipe_output_tuple) > 0:
                    continue #skip water byproduct as a quickfix
                try:
                    item_recipe_lookup_dict[resource_class_name]
                except KeyError:
                    item_recipe_lookup_dict[resource_class_name] = []
                item_recipe_lookup_dict[resource_class_name].append(resource_recipe)           

def create_resource_recipes(machine: machines.machine, allowed_resources: list, recipes_dict: dict, form: str, resources: dict, items_per_minute: float, item_recipe_lookup_dict : dict):
    if len(allowed_resources) == 0:
        for resource_class_name in resources:
            if resources[resource_class_name].get_form() == form:
                allowed_resources.append(resource_class_name) 
    for resource_class_name in allowed_resources:
        resource = resources[resource_class_name]
        recipe_name = resource.get_name() + machine.get_name()
        recipe_input = () # empty tuple
        recipe_output = ((resource, 1),)
        recipe_single_machine_output = items_per_minute
        recipe_machine = machine
        recipe_hard_drive_recipe = False
        recipe_active = False
        if resource.get_name() == 'Water':
            recipe_active = True # Water is nearly infinite

        resource_recipe = recipes.recipe(recipe_name, 
        recipe_output, 
        recipe_input, 
        recipe_single_machine_output, 
        recipe_machine, 
        recipe_hard_drive_recipe, 
        recipe_active)

        recipes_dict[recipe_name] = resource_recipe
        try:
            item_recipe_lookup_dict[resource_class_name]
        except KeyError:
            item_recipe_lookup_dict[resource_class_name] = []
        item_recipe_lookup_dict[resource_class_name].append(resource_recipe)

    
def parse_extractors(extractors_raw: list, machines_dict: dict, recipes_dict: dict, resources: dict, item_recipe_lookup_dict: dict):
    for extractor_dict_full in extractors_raw:
        extractor_display_name = extractor_dict_full['mDisplayName']
        extractor_power = float(extractor_dict_full['mPowerConsumption'])
        extractor_class_name = extractor_dict_full['ClassName']

        allowed_resources = []
        if bool(extractor_dict_full['mOnlyAllowCertainResources']):
            allowed_resources_raw = extractor_dict_full['mAllowedResources']
            if len(allowed_resources_raw) > 0:
                allowed_resources_raw = extractor_dict_full['mAllowedResources'].split(',')
                for resource in allowed_resources_raw:
                    # Split removes every _C so we need to add it back with str.join and add _C at the end
                    resource = str.join('_C',resource.split('.')[-1].split('_C')[0:-1]) + '_C'
                    allowed_resources.append(resource)

        extractor = machines.machine(extractor_display_name, extractor_power, extractor_class_name, False)
        machines_dict[extractor_class_name] = extractor

        items_per_cycle = float(extractor_dict_full['mItemsPerCycle'])
        cycles_per_minute = 60/float(extractor_dict_full['mExtractCycleTime'])
        items_per_minute = items_per_cycle * cycles_per_minute

        allowed_forms = extractor_dict_full['mAllowedResourceForms']
        if 'RF_SOLID' in allowed_forms:
            create_resource_recipes(extractor,allowed_resources, recipes_dict, 'RF_SOLID', resources, items_per_minute, item_recipe_lookup_dict)
        if 'RF_LIQUID' in allowed_forms:
            create_resource_recipes(extractor,allowed_resources, recipes_dict, 'RF_LIQUID', resources, items_per_minute, item_recipe_lookup_dict)
        if 'RF_GAS' in allowed_forms:
            create_resource_recipes(extractor,allowed_resources, recipes_dict, 'RF_GAS', resources, items_per_minute, item_recipe_lookup_dict)

def parse_resources(raw_resources: list, items_dict: dict, resources: dict):
    for resource_dict_full in raw_resources:
        resource_name = resource_dict_full['mDisplayName']
        resource_points = float(resource_dict_full['mResourceSinkPoints'])
        resource_class_name = resource_dict_full['ClassName']
        sinkable = bool(resource_dict_full['mCanBeDiscarded'])
        resource_form = resource_dict_full['mForm']
        resource_energy = float(resource_dict_full['mEnergyValue'])

        resource = items.item(resource_name, resource_points, resource_class_name, sinkable, resource_energy, resource_form)
        items_dict[resource_class_name] = resource
        resources[resource_class_name] = resource

def parse_machine_data(machines_raw: list, machines_dict: dict):
    for machine_dict_full in machines_raw:
            machine_display_name = machine_dict_full['mDisplayName']
            try :
                machine_power = float(machine_dict_full['mEstimatedMaximumPowerConsumption'])
                variable_power = True
            except KeyError:
                machine_power = float(machine_dict_full['mPowerConsumption'])
                variable_power = False
            machine_class_name = machine_dict_full['ClassName']
                
            machine = machines.machine(machine_display_name, machine_power, machine_class_name, variable_power)
            machines_dict[machine_class_name] = machine

def parse_item_data(items_raw: list, items_dict: dict):
    for item_dict_full in items_raw:
        item_name = item_dict_full['mDisplayName']
        item_points = float(item_dict_full['mResourceSinkPoints'])
        item_class_name = item_dict_full['ClassName']
        sinkable = bool(item_dict_full['mCanBeDiscarded'])
        energy = float(item_dict_full['mEnergyValue'])
        form = item_dict_full['mForm']

        item = items.item(item_name, item_points, item_class_name, sinkable,energy,form)
        items_dict[item_class_name] = item

def parse_vanilla_data(json_file):
    json_data = json.load(json_file)

    machines_dict = dict()
    items_dict = dict()
    recipes_dict = dict()

    resources = dict()

    item_recipe_lookup_dict = dict()

    class_dict = dict()
    for class_group in json_data:
        class_group_name = class_group['NativeClass']
        content_list = class_group['Classes']
        class_dict[class_group_name] = content_list

    # Regular machines
    regular_machines  = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableManufacturer'"]
    parse_machine_data(regular_machines, machines_dict)
    variable_power_machines = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableManufacturerVariablePower'"]
    parse_machine_data(variable_power_machines, machines_dict)

    

    
    # Regular items
    regular_items = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGItemDescriptor'"]
    parse_item_data(regular_items, items_dict)
    nuclear_fuel = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGItemDescriptorNuclearFuel'"]
    parse_item_data(nuclear_fuel, items_dict)
    biomass_fuel = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGItemDescriptorBiomass'"]
    parse_item_data(biomass_fuel, items_dict)
    power_shard_and_summer_sloop = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGPowerShardDescriptor'"]
    parse_item_data(power_shard_and_summer_sloop, items_dict)
    equipment = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGEquipmentDescriptor'"]
    parse_item_data(equipment, items_dict)
    alien_power_fuel = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGItemDescriptorPowerBoosterFuel'"]
    parse_item_data(alien_power_fuel, items_dict)
    ammo_projectile = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGAmmoTypeProjectile'"]
    parse_item_data(ammo_projectile, items_dict)
    ammo_instant_hit = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGAmmoTypeInstantHit'"]
    parse_item_data(ammo_instant_hit, items_dict)
    ammo_spreadshot = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGAmmoTypeSpreadshot'"]
    parse_item_data(ammo_spreadshot, items_dict)

    # Resource machines and items
    raw_resources = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGResourceDescriptor'"]
    parse_resources(raw_resources, items_dict, resources)

    resource_extractors = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableResourceExtractor'"]
    parse_extractors(resource_extractors, machines_dict, recipes_dict, resources, item_recipe_lookup_dict)
    water_pump = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableWaterPump'"]
    parse_extractors(water_pump, machines_dict, recipes_dict, resources, item_recipe_lookup_dict)
    Fracking_Extractor = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableFrackingExtractor'"]
    parse_extractors(Fracking_Extractor, machines_dict, recipes_dict, resources, item_recipe_lookup_dict)

    # Generators
    regular_generators = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableGeneratorFuel'"]
    nuclear_generators = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGBuildableGeneratorNuclear'"]
    # implement this later

    # Regular recipes
    regular_recipes = class_dict["/Script/CoreUObject.Class'/Script/FactoryGame.FGRecipe'"]
    parse_recipe(regular_recipes, machines_dict, items_dict, recipes_dict, item_recipe_lookup_dict)

    item_display_name_lookup_dict = {item.get_name(): item for item in items_dict.values()}

    return machines_dict, items_dict, recipes_dict, item_recipe_lookup_dict, item_display_name_lookup_dict

 
if __name__ == "__main__":
    # Setup

    Json_filename = 'Satisfactory.json'
    Json_dir = 'Vanilla data'

    file_dir = os.path.dirname(os.path.abspath(__file__)) # should be .../Source
    json_location = os.path.join(file_dir,Json_dir)
    json_file = os.path.join(json_location, Json_filename)

    with open(json_file, encoding='utf-16') as json_file:
        machines_dict, items_dict, recipes_dict, item_recipe_lookup_dict, item_display_name_lookup_dict = parse_vanilla_data(json_file)

    #### Optimization ####

    # Basic setup
    opti = casadi.Opti()
    opti_variables = dict()
    opti_parameters = dict()
    items_output = dict()
    items_input = dict()

    # User inputs
    requested_outputs = [('SAM Fluctuator', 11.25),('Motor',20), ('Automated Wiring', 10), ('Smart Plating', 100), ('Versatile Framework', 100), ('AI Limiter',20)]
    available_inputs = [('Iron Ore', 3690), ('Copper Ore', 1110), ('Caterium Ore', 540), ('Reanimated SAM', 67.5), ('Steel Beam', 960), ('Water', 20000000)]
    # requested_outputs = [('SAM Fluctuator', 11.25)]
    # Active_alternates = ['Alternate: Iron Pipe']
    Active_alternates = ['Alternate: Fused Quickwire', 'Alternate: Iron Wire', 'Alternate: Fused Wire','Alternate: Caterium Wire','Alternate: Steamed Copper Sheet','Alternate: Iron Pipe','Alternate: Molded Steel Pipe', 'Alternate: Cast Screw', 'Alternate: Steel Screw', 'Alternate: Bolted Iron Plate', 'Alternate: Stitched Iron Plate', 'Alternate: Copper Rotor', 'Alternate: Steel Rotor', 'Alternate: Quickwire Stator', 'Alternate: Bolted Frame', 'Alternate: Steeled Frame']
    goal = 'points'
    # goal = 'power'
    
    # Set active alternates
    for recipe_name in Active_alternates:
        recipe = recipes_dict[recipe_name]
        if not recipe.get_active():
            recipe.toggle_active()

    # Get/Set the requested outputs
    requested_outputs_class_names = [item_display_name_lookup_dict[output[0]].get_class_name() for output in requested_outputs]

    # Get/Set the available inputs

    available_inputs_class_names = [item_display_name_lookup_dict[input[0]].get_class_name() for input in available_inputs]
    for input in available_inputs_class_names:
        item = input[0]
        possible_recipes = item_recipe_lookup_dict[input]
        for recipe in possible_recipes:
            if recipe.get_active(): # recipes replaced by external inputs get auto-disabled, add ability to choose later
                recipe.toggle_active()

    # Activate relevant alternate recipes
    # ...

    # Calctulate the recipe paths
    recipe_paths = []
    for output in requested_outputs_class_names:
        output_item = items_dict[output]
        recipe_paths.append(recipes.calculate_recipe_paths(output_item, item_recipe_lookup_dict))

    optimizer.create_opti_variables(opti, recipe_paths, opti_variables)
    optimizer.create_opti_parameters(opti, opti_variables, opti_parameters, recipes_dict)
    optimizer.add_balance_constraints(opti, opti_variables, opti_parameters, recipes_dict, items_output, items_input)

    sink_points = optimizer.get_sink_points(items_output, items_input, items_dict, available_inputs, item_display_name_lookup_dict) # Iets mis met sink points
    power_consumption = optimizer.get_power_consumption(opti_variables, recipes_dict)

    # Adust parameters
    for item, amount in requested_outputs:
        item_class_name = item_display_name_lookup_dict[item].get_class_name()
        opti.set_value(opti_parameters[item_class_name], amount)
    
    for item, amount in available_inputs:
        item_class_name = item_display_name_lookup_dict[item].get_class_name()
        try:
            opti.set_value(opti_parameters[item_class_name], -amount)
        except KeyError:
            pass # input is not used in any recipe
    
    # Set goal
    if goal == 'points':
        opti.minimize(- sink_points)
    elif goal == 'power':
        opti.minimize(power_consumption)
    else:
        raise ValueError('Goal must be either "points" or "power"')
    
    # Solve and show solution
    opti.solver("ipopt", {"print_time":False}, {"print_level":0, "max_iter":10000})
    solution = opti.solve()
    if goal == 'points':
        print('Sink points:', round(solution.value(sink_points),2))
    elif goal == 'power':
        print('Power consumption:', round(solution.value(power_consumption),2))
    optimizer.print_soltuion(opti_variables, solution, items_output, items_input, items_dict)
    
    
    