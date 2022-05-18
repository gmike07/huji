from ex12.game import *
from ex12.ai import AI
import tkinter
from tkinter import messagebox
from ex12.game import HEIGHT, WIDTH
import time

IMAGE_SIZE = 95
SCREEN_WIDTH = IMAGE_SIZE * 7
RADIUS_DISK = 33
FREE_SPACE = RADIUS_DISK * 2 + 1
SCREEN_HEIGHT = IMAGE_SIZE * 6 + FREE_SPACE
HUMAN = "HUMAN"
ROBOT = "ROBOT"
PLAYER_COLOR = {1: "yellow", 2: "red"}
TITLE = "four in a row"
TITLE_OPTIONS = "game options"
OPTIONS_PLAY = {"  human vs human   ": {1: HUMAN, 2: HUMAN},
                "  human vs robot      ": {1: HUMAN, 2: ROBOT},
                "     robot vs human   ": {1: ROBOT, 2: HUMAN},
                "     robot vs robot      ": {1: ROBOT, 2: ROBOT}}
WIN_TITLE = "WINNER_MESSAGE"
WINNER_MSG = "The player who won is player number: "
TIE_TITLE, TIE_MSG = "TIE MESSAGE", "The game ended in a tie"
PHOTO_FILE = "ex12//cell.png"
BUFFER = 3
WIDTH_LINE = 10
DISC_WIDTH = 3
WAIT_TIME = 200 / 1000


class GUI:
    """
    Class GUI has a players dictionary, game handler object, root, canvas,
    current col and current disc.
    Each GUI handles drawing a single instance of he game
    """
    def __init__(self, players, game_handler):
        """
        Generates a new game GUI with players and a game_handler
        :param players: the players of the game subset of (computer, human)^2
        :param game_handler:
        """
        self.__players = players
        self.__root = tkinter.Tk()  # GUI ROOT
        self.__root.title(TITLE)
        self.__game_handler = game_handler
        # a game cell photo
        #  photo_place = os.path.dirname(os.path.realpath("cell.png"))
        self.photo = tkinter.PhotoImage(master=self.__root,
                                        file=PHOTO_FILE)
        # Generate a canvas for Game Graphics
        self.__root.configure(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.__root.resizable(False, False)
        self.__canvas = tkinter.Canvas(self.__root, width=SCREEN_WIDTH,
                                       height=SCREEN_HEIGHT)
        self.__canvas.pack(fill=tkinter.BOTH, expand=True)
        # add the board made from cells to the canvas
        for row in range(HEIGHT):
            for col in range(WIDTH):
                self.__canvas.create_image(col * IMAGE_SIZE + IMAGE_SIZE / 2,
                                           row * IMAGE_SIZE + FREE_SPACE +
                                           IMAGE_SIZE / 2,
                                           image=self.photo)
        self.curr_disc = None  # current disc played with
        self.curr_col = None  # current column the disc is above
        self.last_call = None
        self.__root.bind("<Motion>", self.follow_mouse)  # follow mouse, draw
        self.__root.bind("<Button-1>", self.click_button)  # follow clicks
        # when the windows is closed call closed()
        self.__root.protocol("WM_DELETE_WINDOW", self.closed)
        self.loop_robot()  # make the robots turns

    def closed(self):
        """
        this function closes the window
        """
        # window was closed, wait waiting time
        self.__root.after_cancel(self.last_call)
        # kill the root
        self.__root.destroy()

    def loop_robot(self):
        """
        this function handles a turn of the ai if it is his turn
        """
        curr_player = self.__game_handler.game.get_current_player()
        if self.__players[curr_player] == ROBOT:  # ROBOT PLAYER
            if not self.__game_handler.game_over():
                # game isn't over yet, do a move
                self.__game_handler.do_move(
                    self.__game_handler.ai.find_legal_move(), True)
        if not self.__game_handler.game_over():
            # game isn't over, do more robot moves
            self.last_call = self.__root.after(1, self.loop_robot)

    def start_loop(self):
        """
        this function starts the gui
        """
        self.__root.mainloop()

    def follow_mouse(self, event):
        """
        :param event: gets a follow mouse event
        this function handles following the mouse and updating the "hover" disc
        accordingly if it is a human
        """
        curr_player = self.__game_handler.game.get_current_player()
        if self.__players[curr_player] == HUMAN:  # HUMAN PLAYER
            x = event.x
            mouse_col = min(int(x / IMAGE_SIZE), WIDTH - 1)
            self.follow_col(mouse_col)  # follow mouse's movement

    def follow_col(self, mouse_col):
        """
        :param mouse_col: gets a col (int)
        this function updating the disc location
        """
        if self.curr_col is not None:  # move the disc to the mouse's column
            diff = int(mouse_col - self.curr_col)
            self.curr_col = mouse_col
            # move disc
            self.__canvas.move(self.curr_disc, IMAGE_SIZE * diff, 0)
        else:  # put a new disc in the first column above the board
            self.curr_col = mouse_col
            self.create_new_disc(self.curr_col)

    def create_new_disc(self, col):
        """
        :param col: gets a col (int)
        this function handles creating a new disc to follow the mouse,
        updates the current col and the current disc
        """
        # new disc location
        x0 = col * IMAGE_SIZE + (IMAGE_SIZE / 2 - RADIUS_DISK)
        x1 = col * IMAGE_SIZE + (IMAGE_SIZE / 2 + RADIUS_DISK)
        y0 = BUFFER
        y1 = 2 * RADIUS_DISK
        curr_player = self.__game_handler.game.get_current_player()
        # Generate new disc of current player at location
        self.curr_disc = self.__canvas.create_oval(x0, y0, x1, y1,
                                                   width=DISC_WIDTH,
                                                   fill=PLAYER_COLOR[
                                                       curr_player])
        self.curr_col = col

    def click_button(self, event):
        """
        :param event: ignored
        this function handles the cilck button event in the game
        """
        curr_player = self.__game_handler.game.get_current_player()
        if self.__players[curr_player] == HUMAN:  # current player HUMAN
            if not self.__game_handler.game_over():  # game isn't over
                # insert a disc in the column, where mouse was pressed
                self.__game_handler.do_move(self.curr_col)

    def make_move(self, row):
        """
        :param row: gets a row (int)
        this function moves the current disc, drops it and then creates the new
        "hover" disc
        """
        diff = IMAGE_SIZE * row + FREE_SPACE + RADIUS_DISK / 2 - BUFFER
        self.__canvas.move(self.curr_disc, 0, diff)  # move disc
        self.create_new_disc(self.curr_col)  # create new disc

    def draw_line(self, location1, location2):
        """
        :param location1: gets a tuple of row, col (int, int)
        :param location2: gets a tuple of row, col (int, int)
        this function draws the "winning" line, from the given coordinates
        """
        row1, col1 = location1
        row2, col2 = location2
        # convert board locations to graphic locations
        x1 = col1 * IMAGE_SIZE + IMAGE_SIZE / 2
        y1 = row1 * IMAGE_SIZE + FREE_SPACE + IMAGE_SIZE / 2
        x2 = (col2 + 1) * IMAGE_SIZE - IMAGE_SIZE / 2
        y2 = row2 * IMAGE_SIZE + FREE_SPACE + IMAGE_SIZE / 2
        # create line (x1,y1) to (x2,y2)
        self.__canvas.create_line(x1, y1, x2, y2, width=WIDTH_LINE)


class MenuGui:
    """
    Class MENU_GUI has a menu gui handler.
    Each MENU_GUI has a root and 4 buttons, and handles creating a game
    """

    def __init__(self):
        self.__root = tkinter.Tk()  # root of GUI
        self.__root.title(TITLE_OPTIONS)  # name it
        for key in OPTIONS_PLAY:  # Create the option buttons
            b = tkinter.Button(self.__root, text=key,
                               command=self.clicked_button(key))
            b.pack()
        self.__root.mainloop()

    @staticmethod
    def clicked_button(key):
        """
        :param key: gets the string the key contains
        :return: a function that creates the new game with the key data
        """

        def start_game():
            """
            Create a game that matches the key pressed by user
            """
            HandleGame(key)

        return start_game


class HandleGame:
    """
    Class Handle_Game has a handle game.
    Each Handle_Game has a game, ai, gui,
    And handles a step of the game and if game is over
    """

    def __init__(self, type_game):
        """
        Generates a new game of four in a row
        :param type_game: the type of game played,
        human or computer against human or computer
        """
        self.game = Game()
        self.ai = AI(self.game)
        self.gui = GUI(OPTIONS_PLAY[type_game], self)  # GUI for game mode
        self.gui.start_loop()

    def game_over(self):
        """
        :return: returns true if the game is over, else false
        """
        return self.game.get_winner() is not None

    def do_move(self, col, is_robot=False):
        """
        :param col: gets a col (int)
        :param is_robot: gets a boolean if the turn is a robot or not
        this function handles a single turn of the game
        """
        try:
            if is_robot:  # current player is a robot, put a disk in the col
                time.sleep(WAIT_TIME)  # sleep before
                self.gui.follow_col(col)  # follow robot's disc movements
            row, col = self.game.make_move(col)  # make the move in game
            self.gui.make_move(row)  # make a move in GUI
            lst = self.game.get_winner_moves()  # winning row
            if lst is not None:  # winning four row exists
                self.gui.draw_line(lst[0], lst[-1])  # draw a line on the row
                tkinter.messagebox.showinfo(WIN_TITLE,
                                            WINNER_MSG + str(
                                                self.game.get_winner()))
            elif self.game_over():  # no winning row, no winner - TIE
                tkinter.messagebox.showinfo(TIE_TITLE, TIE_MSG)
        except:
            pass


if __name__ == '__main__':
    MenuGui()
