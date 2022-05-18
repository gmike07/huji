class Input(object):
    """
    The Input class defines an interface for the game engine to get input
    from the players

    Child classes can use GUI input, CLI input, AI, etc... to produce moves
    """

    input_error_string = "Error: using base input class"

    def get_move(self, player, board):
        """
        Main per-turn function.

        Arguments:
        - player: Which player you are
        - board: A Board object with the current game state
        - pieces: 4 True/False lists describing which pieces each player has left

        Return a Move object if you want to play that move or None if you want
        to pass instead. Passing will be your final move.

        If the returned Move object is illegal, then getMove() will be called
        again with the same arguments.
        """
        raise NotImplementedError(Input.input_error_string)


class RandomInput(Input):
    """RandomInput players choose random moves (equally distributed over piece
    number, x/y, and rotation/flip)
    """

    def get_move(self, player, board):
        import random

        move_list = board.get_legal_moves(player)
        if move_list:
            return move_list[random.randint(0, len(move_list) - 1)]
        # else
        return None
