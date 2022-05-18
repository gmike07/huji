import tkinter
import sys

"""
Classes to control the game's display (screen, GUI, etc)
"""


class Display(object):
    """
    The Display class defines an interface for the game engine to draw the
    game state onto the screen.

    Child classes can use game engine data to draw the game onto the
    command line, on a GUI, etc...
    """

    display_error_string = "Error: using base display class"

    def draw_board(self, board):
        """
        Draw the board onto the screen, command line, etc
        """
        raise NotImplementedError(Display.display_error_string)


class NoDisplay(Display):
    """The NoDisplay doesn't bother drawing the game. Useful for running many
    iterations of the game.
    """

    def draw_board(self, board):
        pass


BLACK = '#%02x%02x%02x' % (int(0 * 255), int(0 * 255), int(0 * 255))
GREY = '#%02x%02x%02x' % (int(0.8 * 255), int(0.8 * 255), int(0.8 * 255))
RED = '#%02x%02x%02x' % (int(1 * 255), int(0 * 255), int(0 * 255))
YELLOW = '#%02x%02x%02x' % (int(1 * 255), int(1 * 255), int(0 * 255))
GREEN = '#%02x%02x%02x' % (int(0 * 255), int(1 * 255), int(0 * 255))
BLUE = '#%02x%02x%02x' % (int(0 * 255), int(0 * 255), int(1 * 255))


class GuiDisplay(Display):
    _width_cell = 20
    _line_width = 2
    _dot_width = 2
    _colors = [RED, YELLOW, GREEN, BLUE]

    def __init__(self, x=20, y=20, color=GREY, title=None):
        self.x = x
        self.y = y
        self._left_click_loc = None
        self._right_click_loc = None
        self._ctrl_left_click_loc = None
        self._keys_down = {}
        self._keys_waiting = {}
        self.prev_state = None
        # This holds an unprocessed key release.  We delay key releases by up to
        # one call to keys_pressed() to get round a problem with auto repeat.
        self._got_release = None

        width = x * GuiDisplay._width_cell + (x + 1) * GuiDisplay._line_width + 1
        height = y * GuiDisplay._width_cell + (y + 1) * GuiDisplay._line_width + 1
        # Save the canvas size parameters
        self._canvas_xs, self._canvas_ys = width, height
        self._canvas_x, self._canvas_y = 0, self._canvas_ys

        self._bg_color = color
        self.kill = False

        # Create the root window
        self._root_window = tkinter.Tk()
        self._root_window.protocol('WM_DELETE_WINDOW', self._destroy_window)
        self._root_window.title(title or 'Graphics Window')
        self._root_window.resizable(0, 0)

        # Create the canvas object
        self._canvas = tkinter.Canvas(self._root_window, width=width, height=height)
        self._canvas.pack()
        self.draw_background()
        self._canvas.update()

        # Bind to key-down and key-up events
        self._clear_keys()

        for i in range(x + 1):
            self.line((1 + GuiDisplay._line_width + i * (GuiDisplay._width_cell + GuiDisplay._line_width), 0),
                      (1 + GuiDisplay._line_width + i * (GuiDisplay._width_cell + GuiDisplay._line_width), height),
                      width=GuiDisplay._line_width)

        for i in range(y + 1):
            self.line((0, 1 + GuiDisplay._line_width + i * (GuiDisplay._width_cell + GuiDisplay._line_width)),
                      (width, 1 + GuiDisplay._line_width + i * (GuiDisplay._width_cell + GuiDisplay._line_width)),
                      width=GuiDisplay._line_width)
        self._canvas.update()

    def line(self, here, there, color=BLACK, width=1):
        x0, y0 = here[0], here[1]
        x1, y1 = there[0], there[1]
        return self._canvas.create_line(x0, y0, x1, y1, fill=color, width=width)

    def _destroy_window(self, _=None):
        if not self.kill:
            self._root_window.destroy()
            self.kill = True
        sys.exit(0)

    def draw_background(self):
        corners = [(0, 0), (0, self._canvas_ys), (self._canvas_xs, self._canvas_ys), (self._canvas_xs, 0)]
        self.polygon(corners, self._bg_color, fill_color=self._bg_color, filled=True, smoothed=False)

    def polygon(self, coords, outline_color, fill_color=None, filled=1, smoothed=1, behind=0, width=1):
        if self.kill:
            self._destroy_window()
        c = []
        for coord in coords:
            c.append(coord[0])
            c.append(coord[1])
        if not fill_color:
            fill_color = outline_color
        if filled == 0:
            fill_color = ""
        poly = self._canvas.create_polygon(c, outline=outline_color, fill=fill_color, smooth=smoothed, width=width)
        if behind > 0:
            self._canvas.tag_lower(poly, behind)  # Higher should be more visible
        return poly

    def _keypress(self, event):
        # remap_arrows(event)
        self._keys_down[event.keysym] = 1
        self._keys_waiting[event.keysym] = 1
        self._got_release = None

    def _keyrelease(self, event):
        # remap_arrows(event)
        del self._keys_down[event.keysym]
        self._got_release = 1

    def _clear_keys(self, _=None):
        self._keys_down = {}
        self._keys_waiting = {}
        self._got_release = None

    def draw_board(self, board, dots=set()):
        if self.kill:
            self._destroy_window()

        state = board.state
        y = len(state)
        assert y == self.y
        x_s = [len(r) for r in state]
        x_max = max(x_s)
        x_min = min(x_s)
        assert x_max == x_min
        assert x_max == self.x

        for i in range(self.y):
            for j in range(self.x):
                if state[i][j] == -1:
                    continue

                if self.prev_state is not None and state[i][j] == self.prev_state[i][j]:
                    continue

                color = GuiDisplay._colors[state[i][j]]
                i_ = self.y - i - 1
                j_ = j
                x = GuiDisplay._line_width + j_ * (GuiDisplay._line_width + GuiDisplay._width_cell) + 2
                y = GuiDisplay._line_width + i_ * (GuiDisplay._line_width + GuiDisplay._width_cell) + 2
                corners = [(x, y),
                           (x + GuiDisplay._width_cell - 1, y),
                           (x + GuiDisplay._width_cell - 1, y + GuiDisplay._width_cell - 1),
                           (x, y + GuiDisplay._width_cell - 1)]

                self.polygon(corners, color, fill_color=color, filled=True, smoothed=False)
        self.prev_state = state.copy()

        for (i, j) in dots:
            i_ = self.y - i - 1
            j_ = j
            x = GuiDisplay._line_width + j_ * (GuiDisplay._line_width + GuiDisplay._width_cell) + int(
                GuiDisplay._width_cell / 2) - int(GuiDisplay._dot_width / 2) + 2
            y = GuiDisplay._line_width + i_ * (GuiDisplay._line_width + GuiDisplay._width_cell) + int(
                GuiDisplay._width_cell / 2) - int(GuiDisplay._dot_width / 2) + 2

            corners = [(x, y),
                       (x + GuiDisplay._dot_width - 1, y),
                       (x + GuiDisplay._dot_width - 1, y + GuiDisplay._dot_width - 1),
                       (x, y + GuiDisplay._dot_width - 1)]
            self.polygon(corners, BLACK, fill_color=BLACK, filled=True, smoothed=True)
        if self.kill:
            self._destroy_window()
        self._canvas.update()
