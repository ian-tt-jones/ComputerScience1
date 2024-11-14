"""
File:    recipe_maker.py
Author:  Ian Jones
Date:    5/06/2021
Section: 33
E-mail:  ijones3L@umbc.edu
Description:
  Used to create the recipe file that the silicon crisis file will access.
"""

import json


def make_cookbook():
    """
    Used to create the recipe file that will be used in the main game. This is created by the user to use in the game.
    
    :return: returns the dictionary that will be loaded into a json file.  
    """
    cookbook = {
        "raw_materials": {},
        "recipes": {}
    }

    raw_material = input("Name the raw material: ")
    raw_materials = {}

    # while loop for raw materials
    while raw_material != "done":
        mine_rate = int(input("Enter the rate at which it is mined: "))
        raw_materials[raw_material] = mine_rate
        raw_material = input("Name the raw material: ")

    # puts the raw materials in the cookbook
    cookbook["raw_materials"] = raw_materials
    output = input("Name the output: ")
    recipes = {}
    # Used to get more data such as recipes and ingredients needed for those recipes
    while output != "done":
        outputs = {}
        output_rate = int(input("Enter the rate at which it is output: "))
        outputs["output"] = output
        outputs["output_count"] = output_rate
        ingredients = {}
        ingredient = input("Name the ingredient: ")
        while (ingredient != "stop") and (ingredient != "done"):
            ingredient_amount = int(input("Amount of that ingredient needed: "))
            ingredients[ingredient] = ingredient_amount
            ingredient = input("Name the ingredient: ")
        outputs["parts"] = ingredients
        recipes[output] = outputs
        output = input("Name the output: ")
    cookbook["recipes"] = recipes
    return cookbook


if __name__ == "__main__":
    # calling the cookbook function to get all the information about materials and recipes
    my_cookbook = make_cookbook()
    
    # getting the filename
    file_name = input("\nEnter the file name: ")

    # Here we are creating the json file where the recipe data will be stored
    write_json_file = open(file_name, "w")
    string_to_write = json.dumps(my_cookbook)
    write_json_file.write(string_to_write)
    write_json_file.close()
