import json
import re

if __name__ == "__main__":
    
    recipes_list = list()
    with open("Source/Vanilla data/vanilla_recipes.json") as vannila_recipes_json:
        
        vanilla_recipes_unpacked = json.load(vannila_recipes_json)
        
        for recipes in vanilla_recipes_unpacked:
            
            recipes_raw_list = recipes['Classes']
            for recipe_dict_full in recipes_raw_list:
                
                recipe_name = recipe_dict_full['mDisplayName']
                recipe_input = recipe_dict_full['mIngredients']
                recipe_output = recipe_dict_full['mProduct']
                recipe_duration = float(recipe_dict_full['mManufactoringDuration'])
                recipe_building = recipe_dict_full['mProducedIn']
                
                hard_drive_recipe = 'Alternate' in recipe_name
                
                recipe_building_list = recipe_building.split(',')
                for building in recipe_building_list:
                    
                    if not "Build_" in building:
                        continue # skip every recipe that isn't made in a building
                    
                    recipe_building_class_name = building.split('.')[-1]
                    
                    recipe_per_minute_multiplier = 60/recipe_duration
                    
                    recipe_output_items_list = []
                    recipe_output_items = recipe_output.split(',')
                    for i in range(len(recipe_output_items)//2):    
                        item_class_name = recipe_output_items[i*2].split('.')[-1]
                        
                        if i == 0:
                            item_amount_per_minute_per_output = 1.0 # is always one because i want to calculate how many input is required to create 1/min of output
                            main_output_amount_string = recipe_output_items[i*2 + 1].split('=')[-1]
                            main_output_amount = float(re.sub("[^0-9\.]", "", main_output_amount_string)) 
                        else:
                            item_amount_string = recipe_output_items[i*2 + 1].split('=')[-1]
                            item_amount_per_minute_per_output =  float(re.sub("[^0-9\.]", "", item_amount_string))  / main_output_amount
                            
                        recipe_output_items_list.append((item_class_name,item_amount_per_minute_per_output))
                        
                    single_machine_output = main_output_amount * recipe_per_minute_multiplier # to calculate the amount of machines needed for a certain amount of main output (= items / (minute*machine))  

                    recipe_input_items_list = []
                    recipe_input_items = recipe_input.split(',')
                    for i in range(len(recipe_input_items)//2):
                        item_class_name = recipe_input_items[i*2].split('.')[-1]
                        
                        item_amount_string = recipe_input_items[i*2 + 1].split('=')[-1]
                        item_amount_per_minute_per_output = float(re.sub("[^0-9\.]", "", item_amount_string)) / main_output_amount
                        
                        recipe_input_items_list.append((item_class_name,item_amount_per_minute_per_output))
                    
                    
                    recipe_dict_select = {
                        'name': recipe_name,
                        'outputs': recipe_output_items_list,
                        'inputs': recipe_input_items_list,
                        'building': recipe_building_class_name,
                        'hard_drive': hard_drive_recipe,
                        'single_machine_output': single_machine_output
                    }
                    recipes_list.append(recipe_dict_select)


    recipes_list.sort(key=lambda x: x['name'])
    # Write the list to a JSON file
    with open("Source/data/recipes.json", "w") as outfile:
        json.dump(recipes_list, outfile, indent=4)