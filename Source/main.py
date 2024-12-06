"""
A planner tool for satisfactory, because the online planners are too limiting.
"""
import json
import os
# import casadi
# custom modules
import modules.recipes as recipes
import modules.items as items
import modules.machines as machines



if __name__ == "__main__":
    # Setup

    file_dir = os.path.dirname(os.path.abspath(__file__)) # should be .../Source
    json_location = os.path.join(file_dir,"data")

    machines_json_path = os.path.join(json_location, "machines.json")
    items_json_path = os.path.join(json_location, "items.json")
    recipes_json_path = os.path.join(json_location, "recipes.json")

    with open(machines_json_path) as machines_json:
        machine_list = json.load(machines_json, object_hook=machines.machine_decoder)

    with open(items_json_path) as items_json:
        items_list = json.load(items_json, object_hook=items.item_decoder)

    item_class_name_lookup_dict = {item.get_class_name(): item for item in items_list}
    item_name_lookup_dict = {item.get_name(): item for item in items_list}
    item_recipe_lookup_dict = {item.get_class_name(): [] for item in items_list}

    with open(recipes_json_path) as recipes_json:
        recipe_list = json.load(recipes_json, object_hook=recipes.recipe_decoder_factory(machine_list, items_list, item_recipe_lookup_dict))
        recipe_list = [recipe for recipe in recipe_list if recipe is not None]

    # Optimization
    # optimizer = casadi.Opti()

    # get the input and output constraints
    output_constraints = []
    input_constraints = []
    
    # calculate the recipe paths
    print(recipes.calculate_recipe_paths(item_name_lookup_dict['Reinforced Iron Plate'], item_recipe_lookup_dict))
    
    