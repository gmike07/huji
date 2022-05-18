import math
TURNING_FACTOR = 7
MAX_LIFE = 3


class Ship:
    """
    this object describes the ship:
     x is the x position of the ship (int)
     y is the y position of the ship (int)
     x_vel is the velocity in the x direction (float)
     y_vel is the velocity in the y direction (float)
     heading is the direction of the ship (int)
     RADIUS is the radius of the ship (int)
     game is the game controlling the ship
     life is the amount of damage the ship can withstand (int)
    """
    def __init__(self, x, y, game, heading=0, x_velocity=0, y_velocity=0):
        """
        this function inits the variables described in the object description,
        if no input is given then heading = x_velocity = y_velocity = 0
        """
        self.__x = x
        self.__y = y
        self.__x_vel = x_velocity
        self.__y_vel = y_velocity
        self.__heading = heading
        self.__RADIUS = 1
        self.__game = game
        self.__life = MAX_LIFE

    def get_x(self):
        """
        :return: returns an int of the position of the ship in the x axis
        """
        return self.__x

    def get_y(self):
        """
        :return: returns an int of the position of the ship in the y axis
        """
        return self.__y

    def get_heading(self):
        """
        :return: returns an int of the rotation of the ship
        """
        return self.__heading

    def get_radius(self):
        """
        :return: returns an int of the radius of the ship
        """
        return self.__RADIUS

    def get_x_vel(self):
        """
        :return: returns a float of the speed of the ship in the x axis
        """
        return self.__x_vel

    def get_y_vel(self):
        """
        :return: returns a float of the speed of the ship in the y axis
        """
        return self.__y_vel

    def update_position(self):
        """
        this function updates the position of the ship
        """
        self.__x, self.__y = self.__game.update_coordinates(self.__x,
                                                            self.__y,
                                                            self.__x_vel,
                                                            self.__y_vel)

    def turn_left(self):
        """
        this function rotates the ship left
        """
        self.__heading -= TURNING_FACTOR

    def turn_right(self):
        """
        this function rotates the ship right
        """
        self.__heading += TURNING_FACTOR

    def accelerate(self):
        """
        this function accelerates the ship (by updating the velocity)
        """
        radians = self.__heading / 180 * math.pi
        self.__x_vel += math.cos(radians)
        self.__y_vel += math.sin(radians)

    def remove_life(self):
        """
        this function reduces the ship's life by 1
        """
        self.__life -= 1

    def get_life(self):
        """
        :return: returns an int of how much life the ship has
        """
        return self.__life

    def teleport(self, x, y):
        """
        :param x: gets a x location
        :param y: gets a y location
        this function teleports the ship to x, y
        """
        self.__x = x
        self.__y = y
