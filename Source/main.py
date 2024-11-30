"""
A planner tool for satisfactory, because the online planners are too limiting.
"""

import json
import os
import sys

# custom modules
import recipes
import items
import machines

working_dir = os.getcwd()
json_location = os.path.join(working_dir,"data")

if __name__ == "__main__":
    with open(json_location + "/vanilla_machines.json") as machines_json:
        mach = json.load(machines_json, object_hook=machines.machine_decoder)
        print(mach)