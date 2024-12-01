import json
import sys


recipes_list = list()
with open("Source/Vanilla export tools/vanilla_recipes.json") as vannila_recipes_json:
    vanilla_recipes_unpacked = json.load(vannila_recipes_json)
    for recipes in vanilla_recipes_unpacked:
        recipes_raw_list = recipes['Classes']
        for recipe_dict_full in recipes_raw_list:
            recipe_name = recipe_dict_full['mDisplayName']
            #...
            recipe_dict_select = {'name': recipe_name, }
            recipes_list.append(recipe_dict_select)


recipes_list.sort(key=lambda x: int(x['points']))
# Write the list to a JSON file
with open("Source\data\recipes.json", "w") as outfile:
    json.dump(recipes_list, outfile, indent=4)