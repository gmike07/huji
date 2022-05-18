from screen import Screen
from ship import Ship
from asteroid import Asteroid
from torpedo import Torpedo
import sys
import random

DEFAULT_ASTEROIDS_NUM = 5
MIN_SPEED, MAX_SPEED = 1, 4
ENEMY_INIT_SIZE = 3
PLAYER_TOOK_DAMAGE = "PLAYER_TOOK_DAMAGE"
MSG_PLAYER_TOOK_DAMAGE = "don't take more damage!"
PLAYER_DIED, MSG_PLAYER_DIED = "you died", "you got hit too many times," \
                                           " try again!"

MSG_PLAYER_QUIT = "don't quit, you lazy gamer!"
PLAYER_QUIT_TITLE = "QUIT ACTION"
VICTORY_TITLE, MSG_VICTORY = "VICTORY", "close and restart the game to play" \
                                        " again"
TORPEDO_LIMIT = 10
SPECIAL_LIMIT = 5
LIMIT_TIME_TORPEDO = 200
SCORE = {2: 50, 1: 100, 3: 20}
LIMIT_TIME_SPECIAL = 150


class GameRunner:
    """
    an object that handles the game,
    has a list of asteroids (Asteroid),
    list of torpedoes (Torpedo)
    a list of special torpedoes (Torpedo objects)
    ship (Ship),
    score (int)
    screen (Screen)
    and the borders of the screen as int
    """
    def __init__(self, asteroids_amount):
        """
        this function gets the number of asteroids to create and inits
            all the things described in the the object description
        """
        self.__screen = Screen()

        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        self.__ship = self.init_ship()
        self.__asteroids = self.init_astreroids(asteroids_amount)
        self.__torpedoes = []
        self.__special_torpedoes = []
        self.draw_game()
        self.__score = 0

    def init_astreroids(self, asteroids_amount):
        """
        :param asteroids_amount: gets an int of the asteroid amount that
            should be created
        :return: a list of new asteroids such that none of them is on the ship
            in random x,y with random speeds and len(list) = asteroids_amount
        """
        asteroids = []
        while len(asteroids) < asteroids_amount:
            x_loc, y_loc = self.random_xy()
            x_speed = random.randint(MIN_SPEED, MAX_SPEED)
            y_speed = random.randint(MIN_SPEED, MAX_SPEED)
            asteroid = Asteroid(x_loc, y_loc, x_speed, y_speed,
                                ENEMY_INIT_SIZE, self)
            if not asteroid.has_intersection(self.__ship):
                asteroids.append(asteroid)
                self.__screen.register_asteroid(asteroid, asteroid.get_size())
        return asteroids

    def random_xy(self):
        """
        :return: returns random x,y from the min of the screen to the max
            of the screen
        """
        x_loc = random.randint(self.__screen_min_x, self.__screen_max_x)
        y_loc = random.randint(self.__screen_min_y, self.__screen_max_y)
        return x_loc, y_loc

    def init_ship(self):
        """
        :return: this function returns a ship object in random location
        """
        x_loc, y_loc = self.random_xy()
        return Ship(x_loc, y_loc, self)

    def draw_game(self):
        """
        this function handles drawing the objects to the screen
        """
        self.__screen.draw_ship(self.__ship.get_x(), self.__ship.get_y(),
                                self.__ship.get_heading())
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.get_x(),
                                        asteroid.get_y())
        self.draw_torpedoes(self.__torpedoes)
        self.draw_torpedoes(self.__special_torpedoes)

    def draw_torpedoes(self, torpedoes):
        """
        :param torpedoes: gets a list of torpedo objects
        this function handles drawing the torpedoess
        """
        for torpedo in torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.get_x(),
                                       torpedo.get_y(), torpedo.get_heading())

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        """
        this function handles the game loop (updates, draws and handles
            victory)
        """
        self.handle_ship_input()
        self.draw_game()
        self.update_objects()
        if len(self.__asteroids) == 0:
            self.__screen.show_message(VICTORY_TITLE, MSG_VICTORY)
            self.game_over()

    def update_objects(self):
        """
        this function updates all objects that are in the game
        """
        self.__ship.update_position()
        self.update_torpedos(self.__torpedoes, LIMIT_TIME_TORPEDO)
        self.update_torpedos(self.__special_torpedoes, LIMIT_TIME_SPECIAL,
                             True)
        self.update_asteroids()
        self.__screen.set_score(self.__score)

    def update_asteroids(self):
        """
        this function handles updating the asteroids
        """
        for asteroid in self.__asteroids:
            asteroid.update_position()
            if asteroid.has_intersection(self.__ship):
                self.__asteroids.remove(asteroid)
                self.ship_hit(asteroid)

    def update_torpedos(self, torpedoes, limit_time, special_torpedo=False):
        """
        :param torpedoes: gets a list of objects (torpedoes)
        :param limit_time: gets a time limit
        :param special_torpedo: gets a boolean if it is a special torpedo
            (default is false)
        this function handles updating the torpedoes
        """
        for torpedo in torpedoes:
            if torpedo.get_spent_time() >= limit_time:
                torpedoes.remove(torpedo)
                self.__screen.unregister_torpedo(torpedo)
            else:
                if special_torpedo:
                    torpedo.update_special(self.__asteroids)
                else:
                    torpedo.update_position()
                for asteroid in self.__asteroids:
                    if asteroid.has_intersection(torpedo):
                        self.handle_colision_torpedo_asteroid(torpedoes,
                                                              torpedo,
                                                              asteroid)

    def handle_colision_torpedo_asteroid(self, torpedoes, torpedo, asteroid):
        """
        :param torpedoes: gets a list of objects (torpedoes)
        :param torpedo: gets a torpedo object
        :param asteroid: gets an asteroid object
        this function handles the collision between the torpedo and asteroid
        """
        if torpedo in torpedoes:
            torpedoes.remove(torpedo)
            self.__screen.unregister_torpedo(torpedo)
        self.__asteroids.remove(asteroid)
        self.__screen.unregister_asteroid(asteroid)
        self.__score += SCORE[asteroid.get_size()]
        if asteroid.get_size() > 1:
            self.split_astroids(torpedo, asteroid)

    def split_astroids(self, torpedo, asteroid):
        """
        :param torpedo: gets a torpedo object
        :param asteroid: gets an asteroid object
        this function handles the spilliting of the asteroid
        """
        speed_x, speed_y = self.get_spilleted_vel(torpedo, asteroid)
        asteroid1 = Asteroid(asteroid.get_x(), asteroid.get_y(),
                             speed_x, speed_y,
                             asteroid.get_size() - 1,
                             self)
        self.__asteroids.append(asteroid1)
        self.__screen.register_asteroid(asteroid1, asteroid1.get_size())
        asteroid2 = Asteroid(asteroid.get_x(), asteroid.get_y(),
                             -1 * speed_x, -1 * speed_y,
                             asteroid.get_size() - 1,
                             self)
        self.__asteroids.append(asteroid2)
        self.__screen.register_asteroid(asteroid2, asteroid2.get_size())

    @staticmethod
    def get_spilleted_vel(torpedo, asteroid):
        """
        :param torpedo: gets a torpedo object
        :param asteroid: gets an asteroid object
        :return: the new speed of the new asteroid that should be created
        """
        mag_square = asteroid.get_x_vel() ** 2 + asteroid.get_y_vel() ** 2
        mag_asteroid = mag_square ** 0.5
        new_speed_x = asteroid.get_x_vel() + torpedo.get_x_vel() / mag_asteroid
        new_speed_y = asteroid.get_y_vel() + torpedo.get_y_vel() / mag_asteroid
        return new_speed_x, new_speed_y

    def ship_hit(self, asteroid):
        """
        :param asteroid: gets an asteroid object
        this function handles the collision between the ship and the asteroid
        """
        self.__ship.remove_life()
        self.__screen.unregister_asteroid(asteroid)
        self.__screen.show_message(PLAYER_TOOK_DAMAGE, MSG_PLAYER_TOOK_DAMAGE)
        self.__screen.remove_life()
        if not self.__ship.get_life() > 0:
            self.__screen.show_message(PLAYER_DIED, MSG_PLAYER_DIED)
            self.game_over()

    def game_over(self):
        """
        this function handles closing the game and deleting all objects from it
        """
        while len(self.__asteroids) > 0:
            self.__screen.unregister_asteroid(self.__asteroids[0])
            self.__asteroids = self.__asteroids[1:]
        self.remove_torpedoes(self.__torpedoes)
        self.remove_torpedoes(self.__special_torpedoes)
        self.__screen.end_game()
        sys.exit()

    def remove_torpedoes(self, torpedoes):
        """
        :param torpedoes: gets a list of torpedoes (Torpedo)
        this function removes all torpedoes from screen
        """
        for torpedo in torpedoes:
            torpedoes.remove(torpedo)
            self.__screen.unregister_torpedo(torpedo)

    def handle_ship_input(self):
        """
        this function handles the user input
        """
        if self.__screen.is_left_pressed():
            self.__ship.turn_left()
        if self.__screen.is_right_pressed():
            self.__ship.turn_right()
        if self.__screen.is_up_pressed():
            self.__ship.accelerate()
        if self.__screen.is_teleport_pressed():
            self.handle_teleport()
        if self.__screen.should_end():
            self.__screen.show_message(PLAYER_QUIT_TITLE, MSG_PLAYER_QUIT)
            self.game_over()
        if self.__screen.is_space_pressed():
            self.handle_add_torpedo(self.__torpedoes, TORPEDO_LIMIT)
        if self.__screen.is_special_pressed():
            self.handle_add_torpedo(self.__special_torpedoes, SPECIAL_LIMIT)

    def handle_add_torpedo(self, torpedoes, limit):
        """
        :param torpedoes: gets a list of torpedoes
        :param limit: gets the limit of the torpedoes
        this function adds a torpedo if it is possible
        """
        if len(torpedoes) < limit:
            torpedo = Torpedo(self.__ship.get_x(), self.__ship.get_y(),
                              self.__ship.get_heading(),
                              self, self.__ship.get_x_vel(),
                              self.__ship.get_y_vel())
            torpedo.accelerate()
            torpedoes.append(torpedo)
            self.__screen.register_torpedo(torpedo)

    def handle_teleport(self):
        """
        this function handles the ship's teleportation
        """
        x_loc, y_loc = self.random_xy()
        self.__ship.teleport(x_loc, y_loc)
        while self.check_colision_asteroids(self.__ship):
            x_loc, y_loc = self.random_xy()
            self.__ship.teleport(x_loc, y_loc)

    def check_colision_asteroids(self, obj):
        """
        :param obj: gets an object (ship or torpedo)
        :return: true if the object has interaction with even 1 asteroid,
            else false
        """
        for asteroid in self.__asteroids:
            if asteroid.has_intersection(obj):
                return True
        return False

    def update_coordinates(self, x, y, speed_x, speed_y):
        """
        :param x: gets an int of x position
        :param y: gets an int of y position
        :param speed_x: gets a float of x speed
        :param speed_y: gets a float of y speed
        :return: the new position x,y as a tuple
        """
        delta_x = self.__screen_max_x - self.__screen_min_x
        delta_y = self.__screen_max_y - self.__screen_min_y
        new_x = int(speed_x + x - self.__screen_min_x)
        new_x = new_x % delta_x + self.__screen_min_x
        new_y = int(speed_y + y - self.__screen_min_y)
        new_y = new_y % delta_y + self.__screen_min_y
        return new_x, new_y


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
