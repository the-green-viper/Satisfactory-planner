import json
import sys


items_list = list()
with open("Source/Vanilla export tools/vanilla_items.json") as vannila_items_json:
    vanilla_items_unpacked = json.load(vannila_items_json)
    for items in vanilla_items_unpacked:
        items_raw_list = items['Classes']
        for item_dict_full in items_raw_list:
            item_name = item_dict_full['mDisplayName']
            item_points = item_dict_full['mResourceSinkPoints']
            item_dict_select = {'name': item_name, 'points': item_points}
            items_list.append(item_dict_select)


items_list.sort(key=lambda x: int(x['points']))
# Write the list to a JSON file
with open("Source\data\items.json", "w") as outfile:
    json.dump(items_list, outfile, indent=4)