import json
import sys

if __name__ == "__main__":
    
    items_list = list()
    with open("Source/Vanilla data/vanilla_items.json") as vannila_items_json:
        
        vanilla_items_unpacked = json.load(vannila_items_json)
        for items in vanilla_items_unpacked:
            
            items_raw_list = items['Classes']
            for item_dict_full in items_raw_list:
                
                item_name = item_dict_full['mDisplayName']
                item_points = item_dict_full['mResourceSinkPoints']
                item_class_name = item_dict_full['ClassName']
                
                #create a dictionary containing current item details so that it can be exported
                item_dict_select = {'name': item_name, 'points': item_points, 'class_name' : item_class_name}
                items_list.append(item_dict_select)

    # sort by sink points because i like the json to be sorted
    items_list.sort(key=lambda x: int(x['points']))
    
    with open("Source/data/items.json", "w") as outfile:
        json.dump(items_list, outfile, indent=4)