VERTICAL_CAR = 0
HORIZONTAL_CAR = 1
DIRECTIONS = {'l': (1, 0), 'r': (-1, 0), "u": (0, -1), "d": (0, 1)}
DIRECTION_HORIZONTAL_VERTICAL = {"u": VERTICAL_CAR, "d": VERTICAL_CAR,
                                 "l": HORIZONTAL_CAR, "r": HORIZONTAL_CAR}
DIRECTION_ORIENTATION = {VERTICAL_CAR: (0, 1), HORIZONTAL_CAR: (1, 0)}
DICT_UP = {"u": "going up is always the good idea",
           "d": "going down solve most errors"}
DICT_LEFT = {"l": "going left is amazing",
             "r": "y would you want to go right?"}
UP, DOWN, LEFT, RIGHT = "u", "d", "l", "r"


class Car:
    """
    Add class description here
    """

    def __init__(self, name, length, location, orientation):
        """
        A constructor for a Car object
        :param name: A string representing the car's name
        :param length: A positive int representing the car's length.
        :param location: A tuple representing the car's head (row, col)
        location
        :param orientation: One of either 0 (VERTICAL) or 1 (HORIZONTAL)
        """
        self.__name = name
        self.__length = length
        self.__orientation = orientation
        x, y = location
        self.__location = y, x

    def car_coordinates(self):
        """
        :return: A list of coordinates the car is in
        """
        lst = []
        x1, y1 = self.__location
        update_x, update_y = DIRECTION_ORIENTATION[self.__orientation]
        for i in range(self.__length):
            lst.append((x1, y1))
            x1, y1 = x1 + update_x, y1 + update_y
        return lst

    def possible_moves(self):
        """
        :return: A dictionary of strings describing possible movements
        permitted by this car.
        """
        if self.__orientation == VERTICAL_CAR:
            return DICT_UP
        else:
            return DICT_LEFT

    def movement_requirements(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: A list of cell locations which must be empty in order for this
        move to be legal.
        """
        x, y = self.__location
        update_x, update_y = DIRECTIONS[movekey]
        return [self.get_next_last_location(x, y, update_x, update_y, movekey)]

    def get_next_last_location(self, x, y, update_x, update_y, movekey):
        """
        :param x: gets a x pos of the car
        :param y: gets a y pos of the car
        :param update_x: gets the x direction in which the car wants to move
        :param update_y: gets the y direction in which the car wants to move
        :param movekey: gets the key the direction of the movement
        :return: a tuple of x, y when x,y are the new location we want the car
            to be in
        """
        if movekey == DOWN or movekey == LEFT:
            return x + self.__length * update_x, y + self.__length * update_y
        return x + update_x, y + update_y

    def move(self, movekey):
        """ 
        :param movekey: A string representing the key of the required move.
        :return: True upon success, False otherwise
        """
        if DIRECTION_HORIZONTAL_VERTICAL[movekey] != self.__orientation:
            return False
        update_x, update_y = DIRECTIONS[movekey]
        x, y = self.__location
        self.__location = x + update_x, y + update_y
        return True

    def get_name(self):
        """
        :return: The name of this car.
        """
        return self.__name
