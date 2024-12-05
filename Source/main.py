"""
A planner tool for satisfactory, because the online planners are too limiting.
"""

import json
import os

# custom modules
# import modules.recipes as recipes
import modules.items as items
import modules.machines as machines



if __name__ == "__main__":

    file_dir = os.path.dirname(os.path.abspath(__file__)) # should be .../Source
    json_location = os.path.join(file_dir,"data")
    machines_json_path = os.path.join(json_location, "machines.json")
    items_json_path = os.path.join(json_location, "items.json")

    with open(machines_json_path) as machines_json:
        machine_list = json.load(machines_json, object_hook=machines.machine_decoder)

    with open(items_json_path) as items_json:
        items_list = json.load(items_json, object_hook=items.item_decoder)