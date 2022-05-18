from .game import *
import random

NO_POS_MOVES = "No possible AI moves"


class AI:
    """
    Class AI has a game object and a player
    this class handles the logic of an ai of the game
    """
    def __init__(self, game, player=1):
        self.__game = game
        self.__player = player

    def find_legal_move(self, timeout=None):
        """
        :param timeout: gets the amount of time to calculate a move
        :return: a legal move of the game, if there is no legal move,
        this function throws an exception
        """
        if self.__game.get_winner() is not None:  # game ended
            raise Exception(NO_POS_MOVES)
            return

        choosing_option = [i for i in range(WIDTH)]
        while len(choosing_option) != 0:  # there are columns to choose from
            choice = random.choice(choosing_option)  # choose a random column
            if self.__game.get_player_at(0, choice) is None:  # col isn't full
                return choice
            choosing_option.remove(choice)
            # choose another row in loop
        # No column to choose from
        raise Exception(NO_POS_MOVES)

    def get_last_found_move(self):
        """
        :return: returns the last found move by the ai
        """
        pass
