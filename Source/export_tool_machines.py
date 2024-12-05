import json
import sys

if __name__ == "__main__":
    
    machines_list = list()
    with open("Source/Vanilla data/vanilla_machines.json") as vannila_machines_json:
        
        vanilla_machines_unpacked = json.load(vannila_machines_json)
        for machines in vanilla_machines_unpacked:
            
            machines_raw_list = machines['Classes']
            for machine_dict_full in machines_raw_list:
                
                machine_name = machine_dict_full['mDisplayName']
                machine_power = float(machine_dict_full['mPowerConsumption'])
                machine_class_name = machine_dict_full['ClassName']
                
                #create a dictionary containing current machine details so that it can be exported
                machine_dict_select = {'name': machine_name, 'power': machine_power, 'class_name' : machine_class_name}
                machines_list.append(machine_dict_select)

    # sort by sink points because i like the json to be sorted
    machines_list.sort(key=lambda x: float(x['power']))
    
    with open("Source/data/machines.json", "w") as outfile:
        json.dump(machines_list, outfile, indent=4)