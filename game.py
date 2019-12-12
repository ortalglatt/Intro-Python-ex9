import helper
import sys
from board import Board
from car import Car

WELCOME_MSG = "Welcome to the Rush Hour game! ENJOY :) \n"
CAR_LENGTH = 0
CAR_LOC = 1
CAR_OR = 2
ORIENTATIONS = [0, 1]
NAMES = ['Y', 'B', 'O', 'W', 'G', 'R']
LENGTH = [2, 3, 4]
DIRECTIONS = ['r', 'l', 'u', 'd']


class Game:
    """
    Class of Game objects, contains the board of the game.
    This class contains all the functions that needed to run a whole game, and
    the function that runs the game.
    """
    RIGHT = "r"
    ONE_MOVE_MSG = "What color car do you want to move, and in what " \
                   "direction \n Please enter it like this- color,direction \n"
    MOVE_LEN = 3
    ERROR_INPUT_MSG = "The input is not valid. Please try again. \n"
    COLOR_ERROR_MSG = "The color you chose doesn't exist on the board. " \
                      "Please try again. \n"
    DIR_ERROR_MSG = "The direction you chose is not valid. Please try again.\n"
    WIN_MSG = "YOU WON! GOOD JOB! :)\n"

    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        :return: None
        """
        self.__board = board

    def __single_turn(self):
        """
        Ask the player to input a car he wants to move and the direction, check
        if the input is valid (if not, prints an error message). If the move
        will win the game, it will print a winning message and exit the game.
        When the player put a valid input, the function will move the car and
        print the current board.
        :return: True if their need to be more single turn.
        """
        move = input(self.ONE_MOVE_MSG)
        if len(move) != self.MOVE_LEN or move[1] != ',':
            print(self.ERROR_INPUT_MSG)
            return
        name, direction = move.split(",")
        if not self.__valid_input(name, direction):
            return
        board.move_car(name, direction)
        print()
        print(board)
        return

    def __valid_input(self, name, direction):
        """
        :param name: the color of the car the player wants to move.
        :param direction: the direction the player wants to move the car to.
        :return: False if the name or the direction are not valid, and True if
        they are valid.
        """
        cars_in_board = []
        for move in self.__board.possible_moves():
            if move[0] not in cars_in_board:
                cars_in_board.append(move[0])
        if name not in cars_in_board:
            print(self.COLOR_ERROR_MSG)
            return False
        pos_moves = [tup[1] for tup in board.possible_moves() if
                     tup[0] == name]
        if direction not in pos_moves:
            print(self.DIR_ERROR_MSG)
            return False
        return True

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(board)
        while self.__board.cell_content(self.__board.target_location()) \
                is None:
            self.__single_turn()
        print(self.WIN_MSG)


def add_cars_to_board(board, filename):
    """
    Create the beginning board of the game.
    :param filename: the json filename with the cars arrange for the game.
    :return: None
    """
    all_cars = helper.load_json(filename)
    for car, lst in all_cars.items():
        if car in NAMES and lst[CAR_LENGTH] in LENGTH \
                and lst[CAR_OR] in ORIENTATIONS:
            car_to_add = Car(car, lst[CAR_LENGTH], lst[CAR_LOC],
                             lst[CAR_OR])
            board.add_car(car_to_add)


if __name__ == "__main__":
    print(WELCOME_MSG)
    filename = sys.argv[1]
    board = Board()
    add_cars_to_board(board, filename)
    game = Game(board)
    game.play()
