"""
File:    board.py
Author:  Ian Jones
Date:    4/30/2021
Section: 33
E-mail:  ijones3@umbc.edu
Description:
  This is the board class for the battleship game.
"""


class Board:
    def __init__(self, board, target_board, player_number):
        self.board = board
        self.target_board = target_board
        self.player_number = player_number
        self.ship_symbol_list = ["Ca", "Ba", "Cr", "Su", "De"]

    def register_shot(self, x, y):
        ship_symbol = self.board[x][y]
        if self.board[x][y] == "  ":
            self.target_board[x][y] = "MM"
            self.board[x][y] = "MM"
            return False, None
        else:
            self.target_board[x][y] = "HH"
            self.board[x][y] = "HH"
            return True, ship_symbol

    def get_ship_name(self, space):
        if space == "Ca":
            return "Carrier"
        elif space == "Ba":
            return "Battleship"
        elif space == "Cr":
            return "Carrier"
        elif space == "Su":
            return "Submarine"
        elif space == "De":
            return "Destroyer"
        else:
            return "error getting ship name"

    def place_ship(self, ship):
        valid_placement = False
        while not valid_placement:
            valid_placement = True
            for place in range(ship.length):
                if ship.direction == "d":
                    if self.board[ship.x][ship.y + place] != "  ":
                        valid_placement = False
                if ship.direction == "r":
                    if self.board[ship.x + place][ship.y] != "  ":
                        valid_placement = False
            if not valid_placement:
                print("invalid placement, try again")
                coordinates = input(f"Enter x y coordinates to place the {ship.name}: ").split()
                direction = input("Enter Right or Down (r or d)")
                ship.direction = direction
                ship.x = int(coordinates[0])
                ship.y = int(coordinates[1])
        for i in range(ship.length):
            if ship.direction == 'd':
                self.board[ship.x + i][ship.y] = f"{ship.name[0]}{ship.name[1]}"
            if ship.direction == 'r':
                self.board[ship.x][ship.y + i] = f"{ship.name[0]}{ship.name[1]}"

    def check_for_winner(self):
        for col in range(len(self.board)):
            for row in range(len(self.board[col])):
                if self.board[col][row] not in self.ship_symbol_list:
                    return False
                else:
                    return True
