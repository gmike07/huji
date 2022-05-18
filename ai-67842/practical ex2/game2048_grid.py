#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    tkGAME - all-in-one Game library for Tkinter

    Gabriele Cirulli's 2048 puzzle game

    Python3-Tkinter port by Raphaël Seban <motus@laposte.net>

    Copyright (c) 2014+ Raphaël Seban for the pr
    esent code

    This program is free software: you can redistribute it and/or
    modify it under the terms of the GNU General Public License as
    published by the Free Software Foundation, either version 3 of
    the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
    General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.

    If not, see http://www.gnu.org/licenses/
"""

# lib imports
import numpy as np
import random

import tkinter as TK

from tkinter import ttk

import game_grid as GG


class Game2048Grid(GG.GameGrid):
    r"""
        Gabriele Cirulli's 2048 puzzle game;

        Python3-Tkinter port by Raphaël Seban;

        GameGrid main component;
    """

    # background color
    # this overrides superclass member

    BGCOLOR = "#ccc0b3"

    # foreground color
    # this overrides superclass member

    FGCOLOR = "#bbada0"

    # nb of rows and columns in grid
    # this overrides superclass member

    ROWS = COLUMNS = 4

    # thickness of a line stroke
    # this overrides superclass member

    THICKNESS = 8  # pixels

    # default global config values
    # this overrides superclass member

    CONFIG = {

        "background": BGCOLOR,

        "highlightthickness": 0,

        "width": 400,  # pixels

        "height": 400,  # pixels

    }  # end of CONFIG

    def __init__(self, master, tile_animation=True, **kw):
        GG.GameGrid.__init__(self, master, **kw)
        self.tile_animation = tile_animation

    def animate_rectangle(self, item_id, value):
        r"""
            GAME OVER animation sequence;

            background rectangle animation;
        """

        self.tag_raise(item_id, TK.ALL)

        self.itemconfigure(item_id, stipple=value)

    # end def

    def animate_text_game_over(self, item_id, value):
        r"""
            GAME OVER animation sequence;

            'Game Over' text animation;
        """

        self.tag_raise(item_id, TK.ALL)

        self.itemconfigure(item_id, fill=value, state=TK.NORMAL)

    # end def

    def animate_text_try_again(self, item_id, value):
        r"""
            GAME OVER animation sequence;

            'Try again' text animation;
        """

        self.tag_raise(item_id, TK.ALL)

        self.itemconfigure(item_id, fill=value, state=TK.NORMAL)

        if value == "#ffffff":
            _btn = ttk.Button(
                self,
                text="Play",
                command=self.owner.new_game
            )

            self.create_window(
                self.winfo_reqwidth() // 2,
                self.winfo_reqheight() // 2 + 65,
                window=_btn,
            )

        # end if

    # end def

    def fuse_tiles(self, into_tile, void_tile):
        r"""
            fuses tile @void_tile into @into_tile and then destroys
            void_tile;

            return True on success, False otherwise;
        """

        # shortcuts

        _into, _void = into_tile, void_tile

        # tiles are matching?

        if _into and _void and (_into.value == _void.value):
            # init new value

            _into.value += _void.value

            # update score with new value

            self.update_score(_into.value)

            # update tile appearance

            _into.update_display()

            # remove void tile

            self.matrix.remove_object_at(*_void.row_column)

            self.remove_tile(_void.id)

            _void.animate_remove()

            # op success

            return True

        # end if - matching tiles

        # op failure

        return False

    # end def

    def game_over(self, tk_event=None, *args, **kw):
        r"""
            shows up game over screen and offers to try again;
        """

        # disconnect keypress events

        self.unbind_all("<Key>")

        # grid dims

        _grid_width = self.winfo_reqwidth()

        _grid_height = self.winfo_reqheight()

        # object inits

        _rect_id = self.create_rectangle(

            0, 0, _grid_width, _grid_height,

            fill=self.FGCOLOR, width=0,
        )

        # animation init

        _anim_rect = GG.GridAnimation(self)

        _anim_rect.register(

            self.animate_rectangle, item_id=_rect_id,
        )

        # do animation

        _anim_rect.start(sequence=("gray12", "gray25", "gray50"))

        # object inits - GAME OVER text

        _text_id = self.create_text(

            _grid_width // 2, _grid_height // 2 - 25,

            text="GAME OVER", font="sans 32 bold", fill="white",

            state=TK.HIDDEN,
        )

        # animation init

        _anim_text1 = GG.GridAnimation(self)

        _anim_text1.register(

            self.animate_text_game_over, item_id=_text_id,
        )

        # do animation

        _anim_text1.start_after(

            delay=800, interval=50,

            sequence=("#c9bdb4", "#d0c5be", "#d7cdc8", "#ded5d2",
                      "#e5dddc", "#ece5e6", "#f3edf0", "#ffffff"),
        )

        # object inits - Try Again text

        _text_id = self.create_text(

            _grid_width // 2, _grid_height // 2 + 30,

            text="Try again", font="sans 16 bold", fill="white",

            state=TK.HIDDEN,
        )

        # animation init

        _anim_text2 = GG.GridAnimation(self)

        _anim_text2.register(

            self.animate_text_try_again, item_id=_text_id,
        )

        # do animation

        _anim_text2.start_after(

            delay=1600, interval=80,

            sequence=("#c9bdb4", "#d0c5be", "#d7cdc8", "#ded5d2",
                      "#e5dddc", "#ece5e6", "#f3edf0", "#ffffff"),
        )

    # end def

    def get_available_box(self):
        r"""
            looks for an empty box location;
        """

        # no more room in grid?

        if self.is_full():

            raise GG.GridError("no more room in grid")

        else:

            _at = self.matrix.get_object_at

            while True:

                _row = random.randrange(self.rows)

                _column = random.randrange(self.columns)

                if not _at(_row, _column):
                    break

                # end if

            # end while

            return (_row, _column)

        # end if - no more room

    # end def

    def init_widget(self, **kw):
        r"""
            widget's main inits;
        """

        # member inits

        self.__score_cvar = TK.IntVar()

        self.__score_callback = None

    # end def

    def move_tile(self, tile, row, column):
        r"""
            moves tile to new (row, column) position;
        """

        # param controls

        if tile:
            # move into matrix

            self.matrix.move_object(tile.row_column, (row, column))

            # make some animation and updates

            tile.animate_move_to(row, column)

        # end if

    # end def

    def move_tiles_down(self):
        r"""
            moves all movable tiles downward;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on columns

        for _column in range(self.columns):

            # pass 1: fusions

            for _row in range(self.rows - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _row2 in range(_row - 1, -1, -1):

                        # get tile

                        _tile2 = _at(_row2, _column)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _row in range(self.rows - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is at least here now

                    _empty = (_empty[0] - 1, _column)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

    # end def

    def move_tiles_left(self):
        r"""
            moves all movable tiles to the left;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on rows

        for _row in range(self.rows):

            # pass 1: fusions

            for _column in range(self.columns - 1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _col in range(_column + 1, self.columns):

                        # get tile

                        _tile2 = _at(_row, _col)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _column in range(self.columns):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is just near last one

                    _empty = (_row, _empty[1] + 1)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

    # end def

    def move_tiles_right(self):
        r"""
            moves all movable tiles to the right;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on rows

        for _row in range(self.rows):

            # pass 1: fusions

            for _column in range(self.columns - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _col in range(_column - 1, -1, -1):

                        # get tile

                        _tile2 = _at(_row, _col)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _column in range(self.columns - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is at least here now

                    _empty = (_row, _empty[1] - 1)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

    # end def

    def move_tiles_up(self):
        r"""
            moves all movable tiles upward;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on columns

        for _column in range(self.columns):

            # pass 1: fusions

            for _row in range(self.rows - 1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _row2 in range(_row + 1, self.rows):

                        # get tile

                        _tile2 = _at(_row2, _column)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _row in range(self.rows):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is at least here now

                    _empty = (_empty[0] + 1, _column)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

    # end def

    def set_game_state(self, game_state):
        rows, cols = np.where(game_state.board != 0)
        for i in range(rows.size):
            self.insert_tile(rows[i], cols[i], game_state.board[rows[i], cols[i]])

    # end def

    def no_more_hints(self):
        r"""
            determines if game is no more playable;

            returns True if game over, False otherwise;
        """

        # verify only at the end

        if self.is_full():

            # enter the Matrix!

            _at = self.matrix.get_object_at

            # loop on rows

            for _row in range(self.rows):

                # loop on columns

                for _column in range(self.columns):

                    # try to find at least *one* fusion to make

                    _tile1 = _at(_row, _column)

                    _tile2 = _at(_row, _column + 1)

                    _tile3 = _at(_row + 1, _column)

                    # compare horizontally

                    if _tile1 and (
                            (_tile2 and _tile1.value == _tile2.value) or
                            (_tile3 and _tile1.value == _tile3.value)):
                        # the show must go on!

                        return False

                    # end if

                # end for - columns

            # end for - rows

            # game is over!

            return True

        # end if - no more room

        # the show must go on!

        return False

    # end def

    def insert_tile(self, row, column, value):
        _tile = Game2048GridTile(self, value, row, column, self.tile_animation)
        _tile.animate_show()
        self.register_tile(_tile.id, _tile)
        self.matrix.add(_tile, *_tile.row_column, raise_error=True)

    def set_score_callback(self, callback, raise_error=False):
        r"""
            sets up a callable function/method to use when updating
            score values;
        """

        if callable(callback):

            self.__score_callback = callback

        elif raise_error:

            raise TypeError(

                "callback parameter *MUST* be a callable object."
            )

        # end if

    # end def

    def tiles_match(self, tile1, tile2):
        r"""
            determines if tiles have the same value;
        """

        return tile1 and tile2 and tile1.value == tile2.value

    # end def

    def update_score(self, value, mode="add"):
        r"""
            updates score along @value and @mode;
        """

        # object is callable?

        if callable(self.__score_callback):
            # update score through callback

            self.__score_callback(value, mode)

        # end if

    # end def


# end class Game2048Grid


# subcomponent class def

class Game2048GridTile(GG.GridTile):
    r"""
        GridTile - GameGrid subcomponent;
    """

    # GridTile colors along internal value

    # color pairs are (background_color, foreground_color)

    COLORS = {

        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024: ("#edc53f", "#f9f6f2"),
        2048: ("#edc22e", "#f9f6f2"),
        4096: ("#ed952e", "#ffe0b7"),
        8192: ("#d2ff50", "#bb6790"),
        16384: ("yellow", "chocolate"),
        32768: ("orange", "yellow"),
        65536: ("red", "white"),

    }  # end of COLORS

    # GridTile fonts along internal value

    FONTS = {

        2: "sans 32 bold",
        4: "sans 32 bold",
        8: "sans 32 bold",
        16: "sans 28 bold",
        32: "sans 28 bold",
        64: "sans 28 bold",
        128: "sans 24 bold",
        256: "sans 24 bold",
        512: "sans 24 bold",
        1024: "sans 20 bold",
        2048: "sans 20 bold",
        4096: "sans 20 bold",
        8192: "sans 20 bold",
        16384: "sans 16 bold",
        32768: "sans 16 bold",
        65536: "sans 16 bold",

    }  # end of FONTS

    def animate_move_to(self, row, column):
        r"""
            animates tile movement to (row, column) destination;

            updates tile's internal data;
        """

        # FIXME: implement true animation by here?

        _x0, _y0 = self.xy_origin

        _x1, _y1 = self.cell_size.xy_left_top(row, column)

        # move tile on canvas

        self.owner.move(self.tag, (_x1 - _x0), (_y1 - _y0))

        # update data

        self.row, self.column = row, column

    # end def

    def animate_tile_popup(self, value):
        r"""
            tile popup animation;
        """

        # init center point

        _x0, _y0 = self.xy_center

        # make animation

        self.owner.scale(self.id, _x0, _y0, value, value)

    # end def

    def animate_remove(self):
        r"""
            animates a grid removal;
        """

        # FIXME: implement true animation by here?

        # remove graphics from canvas

        self.owner.delete(self.tag)

    # end def

    def animate_show(self):
        r"""
            animates tile showing up;
        """

        # create tile

        _x, _y = self.xy_origin

        _width, _height = self.size

        _bg, _fg = self.get_value_colors()

        self.id = self.owner.create_rectangle(

            _x, _y, (_x + _width), (_y + _height),

            fill=_bg, width=0, tags=(self.tag, "tiles"),
        )

        # set value text

        _font = self.get_value_font()

        _x, _y = self.xy_center

        self.value_id = self.owner.create_text(

            _x, _y, text=str(self.value),

            fill=_fg, font=_font, tags=(self.tag, "values"),
        )

        # init animation

        _anim_tile = GG.GridAnimation()

        _anim_tile.register(self.animate_tile_popup)

        # do animation

        _anim_tile.start(

            interval=50, sequence=(6 / 5, 6 / 5, 5 / 6, 5 / 6),
        )

    # end def

    def get_value_colors(self):
        r"""
            returns (background, foreground) color pair along
            internal tile value;
        """

        return self.COLORS.get(self.value, ("red", "yellow"))

    # end def

    def get_value_font(self):
        r"""
            returns font string along internal tile value;
        """

        return self.FONTS.get(self.value, "sans 10 bold")

    # end def

    def update_display(self, tk_event=None, *args, **kw):
        r"""
            updates value display;Game2048GridTile
        """

        # new colors

        _bg, _fg = self.get_value_colors()

        # update tile colors

        self.owner.itemconfigure(self.id, fill=_bg)

        # update tile text and colors

        self.owner.itemconfigure(

            self.value_id,

            text=str(self.value),

            font=self.get_value_font(),

            fill=_fg,
        )

    # end def


# end class Game2048GridTile


class grid_clone():
    r"""
        Gabriele Cirulli's 2048 puzzle game;

        Python3-Tkinter port by Raphaël Seban;

        GameGrid main component;
    """

    # background color
    # this overrides superclass member

    BGCOLOR = "#ccc0b3"

    # foreground color
    # this overrides superclass member

    FGCOLOR = "#bbada0"

    # nb of rows and columns in grid
    # this overrides superclass member

    ROWS = COLUMNS = 4

    # thickness of a line stroke
    # this overrides superclass member

    THICKNESS = 8  # pixels

    # default global config values
    # this overrides superclass member

    CONFIG = {

        "background": BGCOLOR,

        "highlightthickness": 0,

        "width": 400,  # pixels

        "height": 400,  # pixels

    }  # end of CONFIG

    def animate_rectangle(self, item_id, value):
        r"""
            GAME OVER animation sequence;

            background rectangle animation;
        """

        self.tag_raise(item_id, TK.ALL)

        self.itemconfigure(item_id, stipple=value)

    # end def

    def animate_text_game_over(self, item_id, value):
        r"""
            GAME OVER animation sequence;

            'Game Over' text animation;
        """

        self.tag_raise(item_id, TK.ALL)

        self.itemconfigure(item_id, fill=value, state=TK.NORMAL)

    # end def

    def animate_text_try_again(self, item_id, value):
        r"""
            GAME OVER animation sequence;

            'Try again' text animation;
        """

        self.tag_raise(item_id, TK.ALL)

        self.itemconfigure(item_id, fill=value, state=TK.NORMAL)

        if value == "#ffffff":
            _btn = ttk.Button(
                self,
                text="Play",
                command=self.owner.new_game
            )

            self.create_window(
                self.winfo_reqwidth() // 2,
                self.winfo_reqheight() // 2 + 65,
                window=_btn,
            )

        # end if

    # end def

    def fuse_tiles(self, into_tile, void_tile):
        r"""
            fuses tile @void_tile into @into_tile and then destroys
            void_tile;

            return True on success, False otherwise;
        """

        # shortcuts

        _into, _void = into_tile, void_tile

        # tiles are matching?

        if _into and _void and (_into.value == _void.value):
            # init new value

            _into.value += _void.value

            # update score with new value

            self.update_score(_into.value)

            # update tile appearance

            _into.update_display()

            # remove void tile

            self.matrix.remove_object_at(*_void.row_column)

            self.remove_tile(_void.id)

            _void.animate_remove()

            # op success

            return True

        # end if - matching tiles

        # op failure

        return False

    # end def

    def game_over(self, tk_event=None, *args, **kw):
        r"""
            shows up game over screen and offers to try again;
        """

        # disconnect keypress events

        self.unbind_all("<Key>")

        # grid dims

        _grid_width = self.winfo_reqwidth()

        _grid_height = self.winfo_reqheight()

        # object inits

        _rect_id = self.create_rectangle(

            0, 0, _grid_width, _grid_height,

            fill=self.FGCOLOR, width=0,
        )

        # animation init

        _anim_rect = GG.GridAnimation(self)

        _anim_rect.register(

            self.animate_rectangle, item_id=_rect_id,
        )

        # do animation

        _anim_rect.start(sequence=("gray12", "gray25", "gray50"))

        # object inits - GAME OVER text

        _text_id = self.create_text(

            _grid_width // 2, _grid_height // 2 - 25,

            text="GAME OVER", font="sans 32 bold", fill="white",

            state=TK.HIDDEN,
        )

        # animation init

        _anim_text1 = GG.GridAnimation(self)

        _anim_text1.register(

            self.animate_text_game_over, item_id=_text_id,
        )

        # do animation

        _anim_text1.start_after(

            delay=800, interval=50,

            sequence=("#c9bdb4", "#d0c5be", "#d7cdc8", "#ded5d2",
                      "#e5dddc", "#ece5e6", "#f3edf0", "#ffffff"),
        )

        # object inits - Try Again text

        _text_id = self.create_text(

            _grid_width // 2, _grid_height // 2 + 30,

            text="Try again", font="sans 16 bold", fill="white",

            state=TK.HIDDEN,
        )

        # animation init

        _anim_text2 = GG.GridAnimation(self)

        _anim_text2.register(

            self.animate_text_try_again, item_id=_text_id,
        )

        # do animation

        _anim_text2.start_after(

            delay=1600, interval=80,

            sequence=("#c9bdb4", "#d0c5be", "#d7cdc8", "#ded5d2",
                      "#e5dddc", "#ece5e6", "#f3edf0", "#ffffff"),
        )

    # end def

    def get_available_box(self):
        r"""
            looks for an empty box location;
        """

        # no more room in grid?

        if self.is_full():

            raise GG.GridError("no more room in grid")

        else:

            _at = self.matrix.get_object_at

            while True:

                _row = random.randrange(self.rows)

                _column = random.randrange(self.columns)

                if not _at(_row, _column):
                    break

                # end if

            # end while

            return (_row, _column)

        # end if - no more room

    # end def

    def init_widget(self, **kw):
        r"""
            widget's main inits;
        """

        # member inits

        self.__score_cvar = TK.IntVar()

        self.__score_callback = None

    # end def

    def move_tile(self, tile, row, column):
        r"""
            moves tile to new (row, column) position;
        """

        # param controls

        if tile:
            # move into matrix

            self.matrix.move_object(tile.row_column, (row, column))

        # end if

    # end def

    def move_tiles_down(self):
        r"""
            moves all movable tiles downward;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on columns

        for _column in range(self.columns):

            # pass 1: fusions

            for _row in range(self.rows - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _row2 in range(_row - 1, -1, -1):

                        # get tile

                        _tile2 = _at(_row2, _column)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _row in range(self.rows - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is at least here now

                    _empty = (_empty[0] - 1, _column)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

        self.next_tile(acted=_acted)

    # end def

    def move_tiles_left(self):
        r"""
            moves all movable tiles to the left;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on rows

        for _row in range(self.rows):

            # pass 1: fusions

            for _column in range(self.columns - 1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _col in range(_column + 1, self.columns):

                        # get tile

                        _tile2 = _at(_row, _col)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _column in range(self.columns):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is just near last one

                    _empty = (_row, _empty[1] + 1)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

        self.next_tile(acted=_acted)

    # end def

    def move_tiles_right(self):
        r"""
            moves all movable tiles to the right;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on rows

        for _row in range(self.rows):

            # pass 1: fusions

            for _column in range(self.columns - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _col in range(_column - 1, -1, -1):

                        # get tile

                        _tile2 = _at(_row, _col)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _column in range(self.columns - 1, -1, -1):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is at least here now

                    _empty = (_row, _empty[1] - 1)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

        self.next_tile(acted=_acted)

    # end def

    def move_tiles_up(self):
        r"""
            moves all movable tiles upward;
        """

        # inits

        _at = self.matrix.get_object_at

        _acted = False

        # loop on columns

        for _column in range(self.columns):

            # pass 1: fusions

            for _row in range(self.rows - 1):

                # get tile

                _tile1 = _at(_row, _column)

                # got a tile?

                if _tile1:

                    # get next tile

                    for _row2 in range(_row + 1, self.rows):

                        # get tile

                        _tile2 = _at(_row2, _column)

                        # matching values?

                        if self.fuse_tiles(_tile1, _tile2):
                            # we did something

                            _acted = True

                        # end if

                        if _tile2: break

                    # end for - next tile

                # end if - tile

            # end for - fusions

            # empty location inits

            _empty = None

            # pass 2: scrollings

            for _row in range(self.rows):

                # get tile

                _tile1 = _at(_row, _column)

                # new empty location?

                if not _tile1 and not _empty:

                    # empty location is at least here now

                    _empty = (_row, _column)

                # got to move?

                elif _tile1 and _empty:

                    self.move_tile(_tile1, *_empty)

                    # empty location is at least here now

                    _empty = (_empty[0] + 1, _column)

                    # we did something

                    _acted = True

                # end if

            # end for - scrollings

        # end for - row

        # pop-up next tile or game over

        self.next_tile(acted=_acted)

    # end def

    def next_tile(self, tk_event=None, *args, **kw):
        r"""
            verifies if game is over and pops a new tile otherwise;
        """

        # need another new tile?

        if kw.get("acted"):
            # pop up a new tile

            self.pop_tile()

        # end if

        # nothing to play any more?

        if self.no_more_hints():
            # game over!

            self.game_over()

        # end if

    # end def

    def no_more_hints(self):
        r"""
            determines if game is no more playable;

            returns True if game over, False otherwise;
        """

        # verify only at the end

        if self.is_full():

            # enter the Matrix!

            _at = self.matrix.get_object_at

            # loop on rows

            for _row in range(self.rows):

                # loop on columns

                for _column in range(self.columns):

                    # try to find at least *one* fusion to make

                    _tile1 = _at(_row, _column)

                    _tile2 = _at(_row, _column + 1)

                    _tile3 = _at(_row + 1, _column)

                    # compare horizontally

                    if _tile1 and (
                            (_tile2 and _tile1.value == _tile2.value) or
                            (_tile3 and _tile1.value == _tile3.value)):
                        # the show must go on!

                        return False

                    # end if

                # end for - columns

            # end for - rows

            # game is over!

            return True

        # end if - no more room

        # the show must go on!

        return False

    # end def

    def pop_tile(self, tk_event=None, *args, **kw):
        r"""
            pops up a random tile at a given place;
        """

        # ensure we yet have room in grid

        if not self.is_full():
            # must have more "2" than "4" values

            _value = random.choice([2, 2, 2, 2, 2, 2, 2, 2, 2, 4])

            # set grid tile

            _row, _column = self.get_available_box()

            _tile = Game2048GridTile(self, _value, _row, _column)

            # make some animations

            _tile.animate_show()

            # store new tile for further use

            self.register_tile(_tile.id, _tile)

            self.matrix.add(_tile, *_tile.row_column, raise_error=True)

        # end if - room in grid

    # end def

    def set_score_callback(self, callback, raise_error=False):
        r"""
            sets up a callable function/method to use when updating
            score values;
        """

        if callable(callback):

            self.__score_callback = callback

        elif raise_error:

            raise TypeError(

                "callback parameter *MUST* be a callable object."
            )

        # end if

    # end def

    def tiles_match(self, tile1, tile2):
        r"""
            determines if tiles have the same value;
        """

        return tile1 and tile2 and tile1.value == tile2.value

    # end def

    def update_score(self, value, mode="add"):
        r"""
            updates score along @value and @mode;
        """

        # object is callable?

        if callable(self.__score_callback):
            # update score through callback

            self.__score_callback(value, mode)

        # end if

    # end def


# end class Game2048Grid


# subcomponent class def

class Game2048GridTile(GG.GridTile):
    r"""
        GridTile - GameGrid subcomponent;
    """

    # GridTile colors along internal value

    # color pairs are (background_color, foreground_color)

    COLORS = {

        2: ("#eee4da", "#776e65"),
        4: ("#ede0c8", "#776e65"),
        8: ("#f2b179", "#f9f6f2"),
        16: ("#f59563", "#f9f6f2"),
        32: ("#f67c5f", "#f9f6f2"),
        64: ("#f65e3b", "#f9f6f2"),
        128: ("#edcf72", "#f9f6f2"),
        256: ("#edcc61", "#f9f6f2"),
        512: ("#edc850", "#f9f6f2"),
        1024: ("#edc53f", "#f9f6f2"),
        2048: ("#edc22e", "#f9f6f2"),
        4096: ("#ed952e", "#ffe0b7"),
        8192: ("#d2ff50", "#bb6790"),
        16384: ("yellow", "chocolate"),
        32768: ("orange", "yellow"),
        65536: ("red", "white"),

    }  # end of COLORS

    # GridTile fonts along internal value

    FONTS = {

        2: "sans 32 bold",
        4: "sans 32 bold",
        8: "sans 32 bold",
        16: "sans 28 bold",
        32: "sans 28 bold",
        64: "sans 28 bold",
        128: "sans 24 bold",
        256: "sans 24 bold",
        512: "sans 24 bold",
        1024: "sans 20 bold",
        2048: "sans 20 bold",
        4096: "sans 20 bold",
        8192: "sans 20 bold",
        16384: "sans 16 bold",
        32768: "sans 16 bold",
        65536: "sans 16 bold",

    }  # end of FONTS

    def animate_move_to(self, row, column):
        r"""
            animates tile movement to (row, column) destination;

            updates tile's internal data;
        """

        # FIXME: implement true animation by here?

        _x0, _y0 = self.xy_origin

        _x1, _y1 = self.cell_size.xy_left_top(row, column)

        # move tile on canvas

        self.owner.move(self.tag, (_x1 - _x0), (_y1 - _y0))

        # update data

        self.row, self.column = row, column

    # end def

    def animate_tile_popup(self, value):
        r"""
            tile popup animation;
        """

        # init center point

        _x0, _y0 = self.xy_center

        # make animation

        self.owner.scale(self.id, _x0, _y0, value, value)

    # end def

    def animate_remove(self):
        r"""
            animates a grid removal;
        """

        # FIXME: implement true animation by here?

        # remove graphics from canvas

        self.owner.delete(self.tag)

    # end def

    def animate_show(self):
        r"""
            animates tile showing up;
        """

        # create tile

        _x, _y = self.xy_origin

        _width, _height = self.size

        _bg, _fg = self.get_value_colors()

        self.id = self.owner.create_rectangle(

            _x, _y, (_x + _width), (_y + _height),

            fill=_bg, width=0, tags=(self.tag, "tiles"),
        )

        # set value text

        _font = self.get_value_font()

        _x, _y = self.xy_center

        self.value_id = self.owner.create_text(

            _x, _y, text=str(self.value),

            fill=_fg, font=_font, tags=(self.tag, "values"),
        )

        # init animation

        _anim_tile = GG.GridAnimation()

        _anim_tile.register(self.animate_tile_popup)

        # do animation

        if self.tile_animation:
            _anim_tile.start(interval=50, sequence=(6 / 5, 6 / 5, 5 / 6, 5 / 6), )

    # end def

    def get_value_colors(self):
        r"""
            returns (background, foreground) color pair along
            internal tile value;
        """

        return self.COLORS.get(self.value, ("red", "yellow"))

    # end def

    def get_value_font(self):
        r"""
            returns font string along internal tile value;
        """

        return self.FONTS.get(self.value, "sans 10 bold")

    # end def

    def update_display(self, tk_event=None, *args, **kw):
        r"""
            updates value display;
        """

        # new colors

        _bg, _fg = self.get_value_colors()

        # update tile colors

        self.owner.itemconfigure(self.id, fill=_bg)

        # update tile text and colors

        self.owner.itemconfigure(

            self.value_id,

            text=str(self.value),

            font=self.get_value_font(),

            fill=_fg,
        )

    # end def

# end class Game2048GridTile
