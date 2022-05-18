from board import Board
from car import Car
from helper import load_json
import sys
import os.path
ERROR_WRONG_FILE = "you entered a wrong file, FIX \n"
USER_INPUT = "enter a car to move and how to move: \n"
WRONG_NUM_OF_PARAMETERS = "you entered too many , plz fix! \n"
CAR_NAME = 0
CAR_DIR = 1
NUM_ARGS = 2
DIRECTIONS = ["u", "l", "d", "r"]
NAMES = ["Y", "B", "O", "G", "W", "R"]
ERROR_WRONG_DIRECTION = "you entered invalid direction, plz fix! \n"
ERROR_WRONG_NAME = "you entered invalid name, plz fix! \n"
ERROR_CANT_MOVE = "you entered invalid move, plz fix! \n"
DEFAULT_FILE = "car_config.json"
JSON_ENDING = ".json"
VERTICAL_CAR = 0
HORIZONTAL_CAR = 1
GAME_WON = "you won, restart to play again"
MIN_LENGTH, MAX_LENGTH = 2, 4
ERROR_WRONG_LENGTH_JSON = "you gave a wrong length of car! \n"
ERROR_WRONG_OR_JSON = "you gave a wrong orientation of car! \n"
SPILTTER_CONSTANT = ","


class Game:
    """
    Add class description here
    """
    def __init__(self, board):
        """
        Initialize a new Game object.
        :param board: An object of type board
        """
        self.__game_over = False
        self.__board = board
        self.play()

    def __single_turn(self):
        """
        this function plays a single turn of the game
        """
        user_input = input(USER_INPUT).split(SPILTTER_CONSTANT)
        if self.__handle_wrong_input(user_input):
            possible_moves = self.__board.possible_moves()
            name = user_input[CAR_NAME]
            direction = user_input[CAR_DIR]
            if self.__choice_in_possible_moves(name, direction,
                                               possible_moves):
                self.__board.move_car(name, direction)
                print(self.__board)
                self.__handle_game_over()
            else:
                print(ERROR_CANT_MOVE)

    @staticmethod
    def __choice_in_possible_moves(name, direction, possible_moves):
        """
        :param name: gets a car name
        :param direction: gets a direction
        :param possible_moves: gets a list of possible moves
        :return: returns true if the instruction is in possible moves,
            else false
        """
        for move in possible_moves:
            if name in move and direction in move:
                return True
        return False

    def __handle_game_over(self):
        """
        this function changes the game_over if the game is over and prints
            victory if the game is won
        """
        if self.__board.cell_content(self.__board.target_location()) \
                is not None:
            self.__game_over = True
            print(GAME_WON)

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        :return: None
        """
        print(self.__board)
        while not self.__game_over:
            self.__single_turn()

    @staticmethod
    def __handle_wrong_input(user_input):
        """
        :param user_input: gets a user input
        :return: returns true if the input is valid, else returns false and
            prints an error
        """
        if len(user_input) != NUM_ARGS:
            print(WRONG_NUM_OF_PARAMETERS)
            return False
        if user_input[CAR_DIR] not in DIRECTIONS:
            print(ERROR_WRONG_DIRECTION)
            return False
        if user_input[CAR_NAME] not in NAMES:
            print(ERROR_WRONG_NAME)
            return False
        return True


def process_json(filename, board):
    """
    :param filename: gets a string of the file path
    :param board: gets a Board object
    this function adds all the cars in the file to the board if they are valid
    """
    car_config = load_json(filename)
    for name in car_config:
        length, location, orientation = car_config[name]
        if handle_wrong_input(length, orientation):
            board.add_car(Car(name, length, location, orientation))


def handle_wrong_input(length, orientation):
    """
    :param length:  gets an input length
    :param orientation: gets an orientation
    :return: returns true if the inputs are valid, else false and prints error
    """
    if not (MIN_LENGTH <= length <= MAX_LENGTH):
        print(ERROR_WRONG_LENGTH_JSON)
        return False
    if orientation != VERTICAL_CAR and orientation != HORIZONTAL_CAR:
        print(ERROR_WRONG_OR_JSON)
        return False
    return True


def main_program():
    """
    handles the os input and creates the game
    """
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.isfile(filename) or not filename.endswith(JSON_ENDING):
            print(ERROR_WRONG_FILE)
            return
    else:
        filename = DEFAULT_FILE
    board = Board()
    process_json(filename, board)
    Game(board)


if __name__ == "__main__":
    main_program()
