"""
File:    silicon_crisis.py
Author:  Ian Jones
Date:    5/06/2021
Section: 33
E-mail:  ijones3L@umbc.edu
Description:
  Crafts items based on the production of mines to gather raw materials and factories to use those materials to make
  newer items as well as make more mines and factories that can be used to make more items and create an evergrowing
  empire of mines and factories for your own personal wealth.
"""
import json


class Mine:
    def __init__(self, number):
        self.number = number
        self.material = "unassigned"
        self.status = "unassigned"
        self.production_rate = 0

    def mine_materials(self):
        """

        :return: returns the amount of material mined from the mine
        """
        if self.material != "unassigned":
            print("Mining...")
            return self.production_rate

    def set(self, material, recipes):
        """

        :param material: The material that the mine will mine
        :param recipes: The recipes loaded from the json file used to gather information about the material
        :return: does not return anything
        """
        self.material = material
        self.status = "active"
        for materials in recipes["raw_materials"]:
            if materials == material:
                self.production_rate = recipes["raw_materials"][material]


class Factory:
    def __init__(self, number):
        self.number = number
        self.recipe = "unassigned"
        self.status = "unassigned"
        self.production_rate = 0

    def try_to_produce(self, stockpile, recipes):
        """

        :param stockpile: The current stockpile of materials used to check if the factory can produce
        :param recipes: The recipes loaded from the json file to check how much of a material is needed to make it
        :return: Returns what item was made as well as how much of it to track the amounts in the stockpile.
        """
        make_item = True
        if self.status == "active":
            print("Making...")
            for material, value in recipes["recipes"][self.recipe]["parts"].items():
                # checking the raw materials part of stockpile
                if material in stockpile["raw_materials"]:
                    if stockpile["raw_materials"][material] >= value:
                        make_item = True
                    else:
                        return 0, "none"

                # checking the recipes part of stockpile
                if material in stockpile["recipes"]:
                    if stockpile["recipes"][material] >= value:
                        make_item = True
                    else:
                        return 0, "none"
            if make_item:
                return self.production_rate, self.recipe

    def set(self, recipe, recipes):
        """

        :param recipe: The recipe that will be made by the factory
        :param recipes:  The recipes loaded from the json file to get information about the recipes that will be made in
                       the factory
        :return: returns nothing
        """
        self.recipe = recipe
        self.status = "active"
        for a_recipe in recipes["recipes"]:
            if a_recipe == recipe:
                self.production_rate = recipes["recipes"][recipe]["output_count"]


def end_of_turn(list_of_mines, list_of_factories, stockpile, recipes):
    """

    :param list_of_mines: All the mines currently in play
    :param list_of_factories: All the factories currently in play
    :param stockpile: All of the materials and recipes currently mined and made
    :param recipes: The recipes loaded from the json file
    :return: returns the new stockpile as well as a list of items that were produced after the turn
    """
    # this is a list that stores the items produced so they can be saved for later
    items_produced = []
    for mine in range(len(list_of_mines)):
        if list_of_mines[mine].status == "active":
            material_mined = list_of_mines[mine].mine_materials()
            stockpile["raw_materials"][list_of_mines[mine].material] += material_mined
    for fac in range(len(list_of_factories)):
        if list_of_factories[fac].status == "active":
            recipe_made, item_produced = list_of_factories[fac].try_to_produce(stockpile, recipes)
            stockpile["recipes"][list_of_factories[fac].recipe] += recipe_made
            if item_produced != "none":
                items_produced.append(item_produced)
    if len(items_produced) == 0:
        return stockpile, "none"
    else:
        return stockpile, items_produced


def load_recipe_data():
    """

    :return: The json data from the file that was made in recipe_maker.py
    """
    recipe_file = input("Enter SC Recipe File Name: ")
    json_file = open(recipe_file, "r")
    json_data = json_file.read()
    json_file.close()
    recipe_data = json.loads(json_data)
    return recipe_data


def set_stockpile(recipes):
    """

    :param recipes: recipes loaded from the json file. Used to enter in the slots for all the possible items that can
                    be made and mined.
    :return: returns the starting stockpile
    """
    stockpile = {"raw_materials": {}, "recipes": {}}
    for key in recipes["raw_materials"].keys():
        stockpile["raw_materials"][key] = 0
    for key in recipes["recipes"].keys():
        stockpile["recipes"][key] = 0
    return stockpile


def subtract_used_material(stockpile, item_made, recipe):
    """

    :param stockpile: This is the current stockpile of materials
    :param item_made: Item that was made in the round. It's material cost will be subtracted from the stockpile.
    :param recipe: The recipes loaded from the json file to know what the material costs are.
    :return: returns the new stockpile
    """
    material_used = recipe["recipes"][item_made]["parts"]
    for material, value in material_used.items():
        if material in stockpile["raw_materials"].keys():
            stockpile["raw_materials"][material] -= value
        if material in stockpile["recipes"].keys():
            stockpile["recipes"][material] -= value

    return stockpile


def how_many(material, recipe, recipes):
    """
    
    :param material: material to find
    :param recipe: material in recipe
    :param recipes: recipes loaded from json
    :return: returns how many x in a y
    """
    # final result stored here
    result = 0

    # base case
    if recipe in recipes["raw_materials"]:
        return result

    # recursive case
    for key in recipes["recipes"][recipe]:
        result += recipes["recipes"][recipe]["parts"][material]
        for parts in recipes["recipes"][recipe]["parts"]:
            return result + how_many(material, parts, recipes)


if __name__ == "__main__":

    # loads in the recipe data from the file created from the recipe maker
    recipes = load_recipe_data()

    # list of mine objects
    mines = []

    # list of factory objects
    factories = []

    # this is where the stockpile will be stored
    stockpile = set_stockpile(recipes)

    # used to track turns
    turn_count = 1

    # creating the starting mines and factories
    mine_0 = Mine(0)
    mine_1 = Mine(1)
    mines.append(mine_0)
    mines.append(mine_1)
    factory_0 = Factory(0)
    factory_1 = Factory(1)
    factories.append(factory_0)
    factories.append(factory_1)

    action = input("Select Next Action>> ").split()
    while action[0] != "quit":
        # set commands
        if action[0] == "set":
            """
            This section of code deals with making sure the mines are set properly
            and that any mine that is set is not already assigned the same mine number.
            Same for the factories
            
            """
            # setting the mines
            if action[1] == "mine":
                if action[3] in recipes["raw_materials"]:
                    valid_mine = False
                    for mine in range(len(mines)):
                        if (mines[mine].number == int(action[2])) and (mines[mine].material == "unassigned"):
                            valid_mine = True
                    if valid_mine:
                        mines[int(action[2])].set(action[3], recipes)
                else:
                    print("This is not a mineable material")

            # setting the factories
            elif action[1] == "factory":
                if action[3] in recipes["recipes"]:
                    valid_factory = False
                    for factory in range(len(factories)):
                        if (factories[factory].number == int(action[2])) and (factories[factory].recipe == "unassigned"):
                            valid_factory = True
                    if valid_factory:
                        factories[int(action[2])].set(action[3], recipes)
                else:
                    print("This is not a makable recipe")
            action = input("Select Next Action>> ").split()

        # Here is the code for the display commands
        elif action[0] == "display":
            # displaying the factories
            if action[1] == "factories":
                for factory in range(len(factories)):
                    print(f"Factory {factories[factory].number}")
                    print(f"\t{factories[factory].recipe} factory producing {factories[factory].production_rate} per turn")
            # displaying the mines
            elif action[1] == "mines":
                for mine in range(len(mines)):
                    print(f"Mine {mines[mine].number}")
                    print(f"\t{mines[mine].material} mine producing {mines[mine].production_rate} per turn")
            # displaying the stockpile
            elif action[1] == "stockpile":
                print(":::Current Stockpile:::")
                for stock, value in stockpile["raw_materials"].items():
                    print(f"\t{stock}: {value}")
                for stock, value in stockpile["recipes"].items():
                    print(f"\t{stock}: {value}")
            # displaying the raw materials
            elif len(action) == 3:
                if action[1] == "raw":
                    if action[2] == "materials":
                        print(":::Raw Materials:::")
                        for material, value in recipes["raw_materials"].items():
                            print(f"\t{material} - mined in increments of {value}")

            # displaying the recipes
            elif len(action) == 2:
                if action[1] == "recipes":
                    print(":::Recipes:::")
                    for recipe, output in recipes["recipes"].items():
                        output_amount = output["output_count"]
                        print(f"\t{recipe} - produced in increments of {output_amount}")
                        print(f"\tRequired Materials:")
                        for parts, values in output["parts"].items():
                            print(f"\t\t{parts}: {values}")
        # Code for the how many x are in a y command
        elif len(action) == 7:
            if action[0] == "how":
                if action[1] == "many":
                    if action[3] == "are":
                        if action[4] == "in":
                            if action[5] == "a":
                                print(how_many(action[2], action[6], recipes))

            action = input("Select Next Action>> ").split()
        # code for end turn
        elif action[0] == "end":
            if action[1] == "turn" and len(action) == 2:
                # calls an end of turn function
                stockpile, item_made = end_of_turn(mines, factories, stockpile, recipes)

                # this section is used to take away used materials from the stockpile
                if item_made != "none":
                    for items in range(len(item_made)):
                        stockpile = subtract_used_material(stockpile, item_made[items], recipes)
                        if item_made[items] == "mine":
                            new_mine = Mine(len(mines))
                            mines.append(new_mine)
                        if item_made[items] == "factory":
                            new_factory = Factory(len(factories))
                            factories.append(new_factory)
                print(f"Turn {turn_count} Complete")
                turn_count += 1
                action = input("Select Next Action>> ").split()

        # used to quit the program
        elif len(action) == 1 and action[0] != "quit":
            print("Invalid action. Please try again.")
            action = input("Select Next Action>> ").split()

