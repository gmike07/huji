DESCRIPTION_DIR = 0
DESCRIPTION_DESCRIPTION = 1
WINNING_POS = (7, 3)
BOARD_SIZE = 7
EMPTY_LOC = "_" + " "
STAR = "*"
WIN_STRING = "E"
WIN_POS_X = 3
ERROR_ALREADY_HAS_CAR = "you already have a car there, you can't " \
                        "add another one"
WRONG_INPUT_LOCATION = "you entered a wrong car location, plz fix! \n"


class Board:
    """
    Add a class description here.
    Write briefly about the purpose of the class
    """

    def __init__(self):
        """
        this function inits all the cars that the board contains
        """
        self.__cars = []

    def __str__(self):
        """
        This function is called when a board object is to be printed.
        :return: A string of the current status of the board
        """
        lst = self.cell_list()
        s = ""
        for x in range(len(lst)):
            for y in range(len(lst[x])):
                s += lst[x][y]
            s += "\n"
        return s

    def cell_list(self):
        """ This function returns the coordinates of cells in this board
        :return: list of coordinates
        """
        lst = self.__init_list()
        for car in self.__cars:
            positions = car.car_coordinates()
            car_name = car.get_name()
            for position in positions:
                y, x = position
                lst[x][y] = car_name + " "

        for i in range(BOARD_SIZE):
            if i != WIN_POS_X:
                lst[i][-1] = STAR
            else:
                lst[i][-1] = WIN_STRING
        return lst

    @staticmethod
    def __init_list():
        """
        :return: a 2D list of string of an empty board
        """
        lst = []
        for j in range(BOARD_SIZE):
            lst_i = []
            for i in range(BOARD_SIZE + 1):
                lst_i.append(EMPTY_LOC)
            lst.append(lst_i)
        return lst

    def possible_moves(self):
        """ This function returns the legal moves of all cars in this board
        :return: list of tuples of the form (name,movekey,description) 
                 representing legal moves
        """
        possible_moves_lst = []
        for car in self.__cars:
            possible_moves = self.car_possible_moves(car, car.possible_moves())
            possible_moves_lst += possible_moves
        return possible_moves_lst

    def car_possible_moves(self, car, possible_moves_car):
        """
        :param car: gets a Car object
        :param possible_moves_car:  gets a dictionary of the possible car moves
        :return: returns a list of tuples that contain
        (name, direction, description) of all possible moves
        """
        possible_moves = []
        name = car.get_name()
        for direction in possible_moves_car:
            description = possible_moves_car[direction]
            if self.__coordinates_free(car.movement_requirements(direction)):
                possible_moves.append((name, direction, description))
        return possible_moves

    def __coordinates_free(self, coordinates):
        """
        :param coordinates: gets a list of coordinates
        :return: returns true if each of them is in the board and there is
            no other car there
        """
        for coordinate in coordinates:
            x, y = coordinate
            if self.cell_content(coordinate) is not None or \
                    self.__out_of_bounds(x, y):
                return False
        return True

    def target_location(self):
        """
        This function returns the coordinates of the location which is to be
        filled for victory.
        :return: (row,col) of goal location
        """
        return WINNING_POS

    def cell_content(self, coordinate):
        """
        Checks if the given coordinates are empty.
        :param coordinate: tuple of (row,col) of the coordinate to check
        :return: The name if the car in coordinate, None if empty
        """
        for car in self.__cars:
            if coordinate in car.car_coordinates():
                return car.get_name()

    def add_car(self, car):
        """
        Adds a car to the game.
        :param car: car object of car to add
        :return: True upon success. False if failed
        """
        car_to_add_coordinates = car.car_coordinates()
        for coordinate in car_to_add_coordinates:
            if self.cell_content(coordinate) is not None:
                print(ERROR_ALREADY_HAS_CAR)
                return False
        if self.__is_valid_car(car):
            self.__cars.append(car)
            return True
        print(WRONG_INPUT_LOCATION)
        return False

    def __is_valid_car(self, car):
        """
        :param car: gets a Car object
        :return: returns true if all the coordinates of the car are in the
            board
        """
        for location in car.car_coordinates():
            x, y = location
            if self.__out_of_bounds(x, y):
                return False
        return True

    def move_car(self, name, movekey):
        """
        moves car one step in given direction.
        :param name: name of the car to move
        :param movekey: Key of move in car to activate
        :return: True upon success, False otherwise
        """
        for car in self.__cars:
            if car.get_name() == name:
                return car.move(movekey)
        return False

    @staticmethod
    def __out_of_bounds(x, y):
        """
        :param x: gets an int
        :param y: gets an int
        :return: returns false if the coordinate (x,y) is in the board,
            else returns true
        """
        return not (0 <= x <= BOARD_SIZE and 0 <= y <= BOARD_SIZE) \
               and (x, y) != WINNING_POS
