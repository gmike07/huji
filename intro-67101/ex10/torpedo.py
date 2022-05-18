import math

ACCELERATION_FACTOR = 2
MAX_SPEED = 4
X_MOVEMENT = 0
Y_MOVEMENT = 90


class Torpedo:
    """
    this object describes a torpedo:
        x is the x position of the torpedo (int)
        y is the y position of the torpedo (int)
        x_vel is the velocity in the x direction (float)
        y_vel is the velocity in the y direction (float)
        heading is the direction of the torpedo (int)
        RADIUS is the radius of the torpedo (int)
        time_live is how much time past since the torpedo was created (int)
        min_asteroid - if it is a special torpedo, it will be the asteroid
            it will track
        """
    def __init__(self, x, y, heading, game, x_velocity=0, y_velocity=0):
        """
        this function inits the variables described in the object description,
        if no input is given then x_velocity = y_velocity = 0
        """
        self.__x = x
        self.__y = y
        self.__x_vel = x_velocity
        self.__y_vel = y_velocity
        self.__heading = heading
        self.__game = game
        self.__RADIUS = 4
        self.__time_live = 0
        self.__min_asteroid = None

    def get_x(self):
        """
        :return: returns an int of the position of the torpedo in the x axis
        """
        return self.__x

    def get_y(self):
        """
        :return: returns an int of the position of the torpedo in the y axis
        """
        return self.__y

    def get_heading(self):
        """
        :return: returns an int of the rotation of the torpedo
        """
        return self.__heading

    def update_position(self):
        """
        this function updates the position of the torpedo
        """
        self.__x, self.__y = self.__game.update_coordinates(self.__x,
                                                            self.__y,
                                                            self.__x_vel,
                                                            self.__y_vel)
        self.__time_live += 1

    def get_radius(self):
        """
        :return: returns an int of the radius of the torpedo
        """
        return self.__RADIUS

    def accelerate(self):
        """
        this function accelerates the torpedo (by updating the velocity)
        """
        radians = self.__heading / 180 * math.pi
        self.__x_vel += ACCELERATION_FACTOR * math.cos(radians)
        self.__y_vel += ACCELERATION_FACTOR * math.sin(radians)

    def get_spent_time(self):
        """
        :return: returns an int of the time spent living (by this torpedo)
        """
        return self.__time_live

    def get_x_vel(self):
        """
        :return: returns a float of the speed of the torpedo in the x axis
        """
        return self.__x_vel

    def get_y_vel(self):
        """
        :return: returns a float of the speed of the torpedo in the y axis
        """
        return self.__y_vel

    def update_special(self, asteroids):
        """
        :param asteroids: gets a list of asteroids
        this function updates the position of the special shot, which tracks
            the closest asteroid to it
        """
        if len(asteroids) <= 0:
            return
        if self.__time_live == 0:
            self.__min_asteroid = self.get_min_dist_asteroid(asteroids)
        if self.__min_asteroid not in asteroids:
            self.__min_asteroid = self.get_min_dist_asteroid(asteroids)
        x, y = self.__min_asteroid.get_x(), self.__min_asteroid.get_y()
        x1, y1 = x - self.__x, y - self.__y
        if x1 > y1:
            self.__x += min(x1, MAX_SPEED)
            self.__heading = X_MOVEMENT
        else:
            self.__y += min(y1, MAX_SPEED)
            self.__heading = Y_MOVEMENT
        self.__time_live += 1

    def get_min_dist_asteroid(self, asteroids):
        """
        :param asteroids: gets a list of asteroids
        :return: returns the asteroid which is the closest to itself
        """
        min_dist = self.get_dist(asteroids[0].get_x(), asteroids[0].get_y())
        min_asteroid = asteroids[0]
        for asteroid in asteroids:
            if min_dist > min(min_dist, self.get_dist(asteroid.get_x(),
                                                      asteroid.get_y())):
                min_asteroid = asteroid

        return min_asteroid

    def get_dist(self, x, y):
        """
        :param x: gets an int of an x position
        :param y: gets an int of an y position
        :return: returns the distance between this.x, this.y to x,y (float)
        """
        return ((self.__x - x) ** 2 + (self.__y - y) ** 2) ** 0.5
