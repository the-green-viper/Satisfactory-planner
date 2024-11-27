# Object structure
- 3 types of objects:
    1. **Machines**
    2. **Items**
    3. **Recipes**
- Machines are a sub-object of recipes
- Items are a sub-object of recipes
- Maybe a dict to look up what recipes are available for a certain item
## Machines
- Machines stores the name and power consumtion / production
- If a machine consumes power -> power is negative, otherwise positive

## Items 
-Items contain name and the points value

## Recipes 
Contains:
- 