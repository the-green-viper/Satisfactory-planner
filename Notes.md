# Todo 
add recipes for raw rescources
add all machines
look at recipes for power?

# Object structure
- 3 types of objects:
    1. **Machines**
    2. **Items**
    3. **Recipes**
- Machines are a sub-object of recipes
- Items are a sub-object of recipes
- Maybe it makes more sense to use dicts instead of custom objects

## Machines
- Machines stores the name and power consumption / production
- at the moment only consuming buildings are used
- Not yet: (If a machine consumes power -> power is negative, otherwise positive)

## Items 
- Items contain name and the points value

## Recipes 
Contains:
- 
# JSON structure
Right now i'm using a custom format and scripts to export from the 'raw' game json. Might be better to use the game json and do the additional calculations when initializing the objects

# Optimization formula constructor
In order to preform an optimization a formula is needed that gives a one dimensional (=a single number) output based on multiple inputs. This one dimensional output will be either power consumption, total sink points value of the items produced or the amount of single item produced. The formula is a sum of multiple "sub-formulas's" where each sub-formula is a different recipe chain for an item. The inputs for these sub-formula's are the amount of machines used for each step. From these the required raw materials (ores etc.) can be calculated. The amount of additional input items used will also be an input for the formula if available.

## 1. Constraint creation
### Output
Constraints are supplied as a string (in items/min) e.g. "Iron plate >= 500". There are no required opti parameters and NO constraints are added to opti yet.

### Input 
Constraints are supplied as a string (in items/min) e.g. "Iron plate <= 500". There are no required opti parameters and NO constraints are added to opti yet.

## 2. Chain creation
For each output the possible recipe chains are calculated. Then different recipe variables (= input variables of the formula) are created for each path. From the path 3 formula's are made. The outputs of these formula's are the power required, the sink points value of the produced items, the amount of produced items. These formula's should be able to 'compensate' for additional inputs from the input constraints. Example: if a recipe requires iron and coal to create steel but the player already has a steel supply, less iron and coal should be used if the pre-made steel is used.

The recipe variables will be the amount of machines used for each step, these will be stored in a tuple as (recipe, opti_variable).

## 3. Completing the optimizer
The input and output constraints are made based on the different chains and recipe variables. These are also added to opti.
The minimization function is also created together with additional constraints if requested and finally the optimizer is ran.

## 4. Additional considerations
- The workflow is based on output items, in order to optimize for power production all possible fuel sources should be added as requested output items such that recipe chains can be created.
 
