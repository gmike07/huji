EMPTY = None


class Board:
    """
    Class Board has a board builder.
    Each board has a two_dimensional list of numbers and functions to work
    with that data
    """
    def __init__(self, width, height):
        self.__board = [[EMPTY] * width for i in range(height)]
        self.width = width
        self.height = height

    def __contains__(self, location):
        """
        :param location: gets a tuple of location (int), (int)
        :return: returns true if the cell is not empty
        """
        y, x = location
        return self.__board[y][x] != EMPTY

    def get_content(self, y, x):
        """
        :param y: gets a row (int)
        :param x: gets a col (int)
        :return: returns None if the location is out of bounds, else returns
        the content in this location
        """
        if self.out_of_bounds(y, x):  # cell location not in board
            return None
        return self.__board[y][x]  # cell content

    def update_location(self, y, x, player):
        """
        this function updates the location with the player's value
        :param y: gets a row (int)
        :param x: gets a col (int)
        :param player: gets the player that wants to insert his disc in this
        location
        """
        self.__board[y][x] = player

    def out_of_bounds(self, y, x):
        """
        :param y: gets a row (int)
        :param x: gets a col (int)
        :return: returns false if the location is in bounds else true
        """
        return not (0 <= y < self.height and 0 <= x < self.width)
