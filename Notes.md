# Object structure
- 3 types of objects:
    1. **Machines**
    2. **Items**
    3. **Recipes**
- Machines are a sub-object of recipes
- Items are a sub-object of recipes
- Maybe a dict to look up what recipes are available for a certain item
## Machines
- Machines stores the name and power consumption / production
- If a machine consumes power -> power is negative, otherwise positive

## Items 
-Items contain name and the points value

## Recipes 
Contains:
- 
# JSON structure
Right now i'm using a custom format and scripts to export from the 'raw' game json. Might be better to use the game json and do the additional calculations when initializing the objects