"""
File:    battleship.py
Author:  Ian Jones
Date:    4/25/2021
Section: 33
E-mail:  ijones3@umbc.edu
Description:
  This is the game battleship.
"""
import board

BOARD_LENGTH = 10


class BattleshipGame:
    player_1_board = board.Board(
        [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]],

        [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]],"player_1")

    player_2_board = board.Board(
        [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]],

        [["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "],
         ["  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  "]], "player_2")

    current_turn = 0

    player_1_ships = []
    player_2_ships = []

    game_over = False

    def __init__(self, size=10):
        self.size = size

    # places the ships on the board
    def place_ships(self, player):
        num_of_ships = 5
        name = ""
        length = ""
        for ship_to_place in range(num_of_ships):
            self.display_boards(self.current_turn, player.board, "")
            if ship_to_place == 0:
                length = 5
                name = "Carrier"
            elif ship_to_place == 1:
                length = 4
                name = "Battleship"
            if ship_to_place == 2:
                length = 3
                name = "Cruiser"
            if ship_to_place == 3:
                length = 3
                name = "Submarine"
            if ship_to_place == 4:
                length = 2
                name = "Destroyer"
            coordinates = input(f"Enter x y coordinates to place the {name}: ").split()
            while (int(coordinates[0]) > 9 or int(coordinates[0]) < 0) or \
                    (int(coordinates[1]) > 9 or int(coordinates[1]) < 0):
                print("Coordinates must be between 0 and 9")
                coordinates = input(f"Enter x y coordinates to place the {name}: ").split()

            direction = input("Enter Right or Down (r or d)")
            while direction != "r" and direction != "d":
                print("Only enter r or d for direction")
                direction = input("Enter Right or Down (r or d)")

            ship = Ships(name, length, int(coordinates[0]), int(coordinates[1]), direction)
            if player.player_number == "player_1":
                self.player_1_ships.append(ship)
                self.player_1_board.place_ship(ship)
            elif player.player_number == "player_2":
                self.player_2_ships.append(ship)
                self.player_2_board.place_ship(ship)

    # displays the board
    def display_boards(self, turn, board1, board2):
        if self.current_turn == 0:
            print("\n")
            top_row = [" 0", " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
            for num in range(BOARD_LENGTH):
                print(top_row[num], end=" ")
            for col in range(BOARD_LENGTH):
                print("\n")
                for row in range(BOARD_LENGTH):
                    if row == 0:
                        print(col, end="")
                    print(board1[col][row], end="|")
            print("\n")
        else:
            print("\n")
            top_row = [" 0", " 1", " 2", " 3", " 4", " 5", " 6", " 7", " 8", " 9"]
            for num in range(BOARD_LENGTH):
                print(top_row[num], end=" ")
            print("\t\t\t\t", end="")
            for num in range(BOARD_LENGTH):
                print(top_row[num], end=" ")

            for col in range(BOARD_LENGTH):
                print("\n")
                for row in range(BOARD_LENGTH):
                    if row == 0:
                        print(col, end="")
                    print(board1[col][row], end="|")
                print("\t\t\t\t", end="")
                for row in range(BOARD_LENGTH):
                    if row == 0:
                        print(col, end="")
                    print(board2[col][row], end="|")
            print("\n")

    def run_game(self):
        # this is the ship placing phase
        for i in range(2):
            if i == 0:
                print("Player 1, prepare to place your fleet.")
                self.place_ships(self.player_1_board)
            elif i == 1:
                print("Player 2, prepare to place your fleet.")
                self.place_ships(self.player_2_board)
        self.display_boards(self.current_turn, self.player_2_board.board, "")
        self.current_turn = 1

        # main game loop
        while not self.game_over:
            target_coordinates = input("Enter your target coordinates(enter quit to quit): ").split()
            if target_coordinates[0] != "quit":
                if self.current_turn % 2 == 1:
                    while self.player_1_board.board[int(target_coordinates[0])][int(target_coordinates[1])] == "HH":
                        print("You already shot there, try again")
                        target_coordinates = input("Enter your target coordinates: ").split()
                    while self.player_1_board.board[int(target_coordinates[0])][int(target_coordinates[1])] == "MM":
                        print("You already shot there, try again")
                        target_coordinates = input("Enter your target coordinates: ").split()

                    # displays target and player boards
                    self.display_boards(self.current_turn, self.player_2_board.target_board, self.player_1_board.board)
                    self.display_boards(self.current_turn, self.player_1_board.target_board, self.player_1_board.board)
                    did_hit, ship_hit = self.player_2_board.register_shot(int(target_coordinates[0]),
                                                                          int(target_coordinates[1]))

                    # continues accordingly if hit or no hit
                    if did_hit:
                        print(f"Hit! You hit the {ship_hit}")
                    else:
                        print("Your shot was a miss!")
                    if self.player_2_board.check_for_winner():
                        print("Player 1 is the winner!")
                        self.game_over = True
                    self.current_turn += 1
                else:
                    while self.player_1_board.board[int(target_coordinates[0])][int(target_coordinates[1])] == "HH":
                        print("You already shot there, try again")
                        target_coordinates = input("Enter your target coordinates: ").split()
                    while self.player_1_board.board[int(target_coordinates[0])][int(target_coordinates[1])] == "MM":
                        print("You already shot there, try again")
                        target_coordinates = input("Enter your target coordinates: ").split()
                    self.display_boards(self.current_turn, self.player_2_board.target_board, self.player_1_board.board)

                    did_hit, ship_hit = self.player_1_board.register_shot(int(target_coordinates[0]),
                                                                          int(target_coordinates[1]))
                    if did_hit:
                        print(f"Hit! You hit the {ship_hit}")
                    else:
                        print("Your shot was a miss!")
                    if self.player_1_board.check_for_winner():
                        print("Player 2 is the winner!")
                        self.game_over = True
                    self.current_turn += 1
            else:
                self.game_over = True


class Ships:
    def __init__(self, name, length, x, y, direction):
        self.name = name
        self.length = length
        self.x = x
        self.y = y
        self.direction = direction


if __name__ == "__main__":
    BattleshipGame().run_game()
