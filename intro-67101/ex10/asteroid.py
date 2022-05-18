import math
SCALE_FACTOR = 10
NORMALIZING_FACTOR = 5


class Asteroid:
    """
        this object describes an asteroid:
         x is the x position of the asteroid (int)
         y is the y position of the asteroid (int)
         x_vel is the velocity in the x direction (float)
         y_vel is the velocity in the y direction (float)
         size is the size of the asteroid (int)
         radius is the radius of the asteroid (int)
         game is the game controlling the asteroid
        """
    def __init__(self, x, y, x_velocity, y_velocity, size, game):
        """
        this function inits the variables described in the object description
        """
        self.__x = x
        self.__y = y
        self.__x_vel = x_velocity
        self.__y_vel = y_velocity
        self.__size = size
        self.__radius = SCALE_FACTOR * size - NORMALIZING_FACTOR
        self.__game = game

    def get_x(self):
        """
        :return: returns an int of the position of the asteroid in the x axis
        """
        return self.__x

    def get_y(self):
        """
        :return: returns an int of the position of the asteroid in the y axis
        """
        return self.__y

    def get_radius(self):
        """
        :return: returns an int of the radius of the asteroid
        """
        return self.__radius

    def get_size(self):
        """
        :return: returns an int of the size of the asteroid
        """
        return self.__size

    def has_intersection(self, obj):
        """
        :param obj: gets an object (torpedo or ship)
        :return: true if has collision with the object, else false
        """
        distance_x = self.get_x() - obj.get_x()
        distance_y = self.get_y() - obj.get_y()
        dist = math.hypot(distance_x, distance_y)
        return dist <= self.get_radius() + obj.get_radius()

    def update_position(self):
        """
        this function updates the position of the asteroid
        """
        self.__x, self.__y = self.__game.update_coordinates(self.__x,
                                                            self.__y,
                                                            self.__x_vel,
                                                            self.__y_vel)

    def get_x_vel(self):
        """
        :return: returns a float of the speed of the asteroid in the x axis
        """
        return self.__x_vel

    def get_y_vel(self):
        """
        :return: returns a float of the speed of the asteroid in the y axis
        """
        return self.__y_vel
