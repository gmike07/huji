from .board import *

WIN_LENGTH = 4
WIDTH = 7
HEIGHT = 6
PLAYER_ONE = 1
PLAYER_TWO = 2
REPLACE_PLAYER = {PLAYER_ONE: PLAYER_TWO, PLAYER_TWO: PLAYER_ONE}
TIE = 0
ILLEGAL_MOVE = "Illegal move"
RANGE_X = range(-1, 2)
RANGE_Y = range(-1, 2)


class Game:
    """
    Class Game has a game builder.
    Each Game has a board, current player, state of game, winner and
    number of moves
    And super cool functions(:
    """

    def __init__(self):
        self.__board = Board(WIDTH, HEIGHT)
        self.__player = PLAYER_ONE
        self.__game_over = False
        self.__winner = TIE
        self.__num_moves = 0
        self.__winner_moves = None

    def make_move(self, column):
        """
        :param column: gets a col that the player desires to add a disc to(int)
        this function makes a single move on the board and throws an error
        if the move is invalid
        :return: returns None with exception if an error occurred, else
        returns a tuple of row, col that was updated ((int),(int))
        """
        # game finished or column is full
        if (0, column) in self.__board or self.__game_over:
            raise Exception(ILLEGAL_MOVE)
        row = self.__find_index(column)  # find first empty cell in column
        # put the player's disc in the location
        self.__board.update_location(row, column, self.__player)
        self.__num_moves += 1  # increase the number of moves played in game
        self.update_game_over(row, column)  # check if game is over
        self.__player = REPLACE_PLAYER[self.__player]  # change current player
        return row, column  # return the location that a disc was added to

    def update_game_over(self, row, col):
        """
        :param row: gets a row (int)
        :param col: gets a col (int)
        this function handles the game over
        """
        if self.__num_moves == WIDTH * HEIGHT:  # Board is full
            self.__game_over = True
            return
        for i in RANGE_Y:
            for j in RANGE_X:
                # check if the player has 4 in a row in y,x - (j,i) direction
                if not (i == 0 and j == 0) and self.check_win(row, col, i, j):
                    self.__winner = self.__player
                    self.__game_over = True
                    return

    def check_win(self, row, col, i, j):
        """
        :param row: gets a row (int)
        :param col: gets a col (int)
        :param i: gets the y direction (int)
        :param j: gets the x direction (int)
        :return: returns true if the player won this round, else false
        """
        # check if the player won the game in this direction
        return self.winner(row, col, i, j) or self.winner(row - i, col - j, i,
                                                          j) \
               or self.winner(row - 2 * i, col - 2 * j, i, j)

    def winner(self, row, col, y, x):
        """
        :param row: gets a row (int)
        :param col: gets a col (int)
        (row, col) = starting point to check win from
        :param y: gets the y direction (int)
        :param x: gets the x direction (int)
        :return: returns true if current player won the game in
        the y,x direction, else false
        """
        # runs on cells in the direction and checks if the player won the game
        for k in range(WIN_LENGTH):
            if self.get_player_at(row, col) != self.__player:
                return False  # different disc, No four in a row in direction
            row, col = row + y, col + x  # go to next cell
        lst = []
        row, col = row - y, col - x
        for k in range(WIN_LENGTH):  # add the winner's winning row
            lst.append((row, col))
            row, col = row - y, col - x
        self.__winner_moves = lst  # put the winning row in the four in a row
        return True

    def get_winner_moves(self):
        """
        :return: sorts the winning moves list from min to max and
        returns the sorted list
        """
        if self.__winner_moves is None:
            return
        # sort the winner moves
        for i in range(len(self.__winner_moves)):
            for j in range(i + 1, len(self.__winner_moves)):
                if self.__winner_moves[i] > self.__winner_moves[j]:
                    self.__winner_moves[i], self.__winner_moves[j] = \
                        self.__winner_moves[j], self.__winner_moves[i]
        return self.__winner_moves

    def __find_index(self, column):
        """
        :param column: gets a col (int)
        :return: returns the first empty row in this column
        """
        for i in range(HEIGHT - 1, -1, -1):
            if not (i, column) in self.__board:  # place i in column is empty
                return i

    def get_winner(self):
        """
        :return: returns None if the game isn't over yet,
        else,the winner if exists
        else, Tie
        """
        if not self.__game_over:  # game not over yet
            return None
        else:  # game over
            return self.__winner

    def get_player_at(self, row, col):
        """
        :param row: gets a row (int)
        :param col: gets a col (int)
        :return: returns None if the location is out of bounds, else returns
        the content in this location
        """
        return self.__board.get_content(row, col)

    def get_current_player(self):
        """
        :return: returns the current player that should make a move
        """
        return self.__player
