# Object structure
- 3 types of objects:
    1. **Machines**
    2. **Items**
    3. **Recipes**
- Machines are a sub-object of recipes
- Items are a sub-object of recipes
- Maybe a dict to look up what recipes are available for a certain item
- Maybe it makes more sense to use dicts instead of custom objects

## Machines
- Machines stores the name and power consumption / production
- at the moment only consuming buildings are used
- Not yet: (If a machine consumes power -> power is negative, otherwise positive)

## Items 
-Items contain name and the points value

## Recipes 
Contains:
- 
# JSON structure
Right now i'm using a custom format and scripts to export from the 'raw' game json. Might be better to use the game json and do the additional calculations when initializing the objects

# Optimization formula constructor
In order to preform an optimization a formula is needed that gives a one dimensional (=a single number) output based on multiple inputs. This one dimensional output will be either power consumption, total sink points value of the items produced or the amount of single item produced. The formula is a sum of multiple "sub-formulas's" where each sub-formula is a different recipe chain for an item. The inputs for these sub-formula's are the raw resources (ore's and such) and other items specified in the constraints as inputs.

1. We start from the requested output items. These are specified in the constraints
2. For each output items the possible recipe chains are created as list containing the recipe object.
3. For each recipe path 3 formula's are !! SOMEHOW !! made. The outputs of these formula's are the power required, the sink points value of the produced items, the amount of produced items.
4. The different recipes for every chain will be combined to create the main optimization formula or in order to check the constraints

The above workflow is not suitable for power production as it assumes an output item. It may be possible to require to select a certain energy source. Another approach could also be to consider all possible energy sources as requested items, this would require to set a constraint on every raw resource. 

## 1. Constraint creation
### Output
Constraints are supplied as a string (in items/min) e.g. "Iron plate >= 500". The required opti parameters are created and the constraints are added to opti.
### Input 
Constraints are supplied as a string (in items/min) e.g. "Iron plate <= 500". The opti variables are NOT yet made and NO constraints are added to opti yet.

## 2. Chain creation
For each output the possible recipe chains are calculated. Then different input variables are created for each path. From the path 3 formula's are made. The outputs of these formula's are the power required, the sink points value of the produced items, the amount of produced items. These formula's should be able to 'compensate' for additional inputs from the input constraints e.g. if a recipe requires iron and coal to create steel but the player already has a steel supply, less iron and coal should be used if the pre-made steel is used.
