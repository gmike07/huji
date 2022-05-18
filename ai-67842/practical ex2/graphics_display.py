#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
tkGAME - all-in-one Game library for Tkinter

Gabriele Cirulli's 2048 puzzle game

Python3-Tkinter port by Raphaël Seban <motus@laposte.net>

Copyright (c) 2014+ Raphaël Seban for the present code

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
import tkinter as TK
import tkinter.messagebox
import weakref

from tkinter import ttk
import game2048_grid as GG
from game import Action


class GameScore(ttk.Frame):
    r"""
        GameScore - Game subcomponent;
    """

    # default global config values

    CONFIG = {

        "padding": "10px",

    }  # end of CONFIG

    def __init__(self, master=None, **kw):
        self.CONFIG = self.CONFIG.copy()
        self.CONFIG.update(kw)
        # super class inits

        ttk.Frame.__init__(self, master)

        self._cvar = TK.IntVar()
        self.configure(**self._only_tk(self.CONFIG))
        self._tk_owner = master
        self.init_widget(**self.CONFIG)

    def _only_tk(self, kw):
        r"""
            protected method def;

            filters external keywords to suit tkinter init options;

            returns filtered dict() of keywords;
        """

        # inits

        _dict = dict()

        # $ 2014-03-24 RS $
        # Caution:
        # TK widget *MUST* be init'ed before calling _only_tk() /!\
        # self.configure() needs self.tk to work well

        if hasattr(self, "tk") and hasattr(self, "configure"):

            _attrs = set(self.configure().keys()) & set(kw.keys())

            for _key in _attrs:
                _dict[_key] = kw.get(_key)

            # end for

        # end if

        return _dict

    # end def

    def add_score(self, value):
        r"""
            adds value to current score value;
        """

        self._cvar.set(

            self._cvar.get() + abs(int(value))
        )

    # end def

    def get_score(self):
        r"""
            returns current score value;
        """

        return self._cvar.get()

    # end def

    def high_score(self, value):
        r"""
            replaces current score value by @value if greater;
        """

        self._cvar.set(max(self._cvar.get(), int(value)))

    # end def

    def init_widget(self, **kw):
        r"""
            hook method to override in subclass;

            widget's main inits;
        """
        self.reset_score()
        self.score_label = ttk.Label(self, text=kw.get("label", "Score:"))
        self.score_label.pack(side=TK.LEFT)
        self.score_display = ttk.Label(self, textvariable=self._cvar)
        self.score_display.pack(side=TK.RIGHT)

    # end def

    def reset_score(self):
        r"""
            resets current score value to zero;
        """

        self._cvar.set(0)

    def set_score(self, value):
        r"""
            replaces current score value;
        """
        self._cvar.set(int(value))

    def sub_score(self, value):
        r"""
            substracts value from current score value;
        """
        self._cvar.set(self._cvar.get() - abs(int(value)))


class GabrieleCirulli2048GraphicsDisplay(TK.Tk):
    r"""
    Gabriele Cirulli's 2048 puzzle game;

    Python3-Tkinter port by Raphaël Seban;
    """

    def __init__(self, new_game_callback, quit_game_callback, human_agent):
        super(GabrieleCirulli2048GraphicsDisplay, self).__init__()
        self._new_game_callback = new_game_callback
        self._quit_game_callback = quit_game_callback
        self._padding = 10
        self.game_state = None
        self._keyboard_pressed_observers = []
        self._build_ui(human_agent)

    def _build_ui(self, human_agent):
        self.title("Intro to AI -- EX2")
        self.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.resizable(width=False, height=False)
        # look'n'feel
        ttk.Style().configure(".", font="sans 10")
        # get 2048's grid
        self.grid = GG.Game2048Grid(self, tile_animation=human_agent)
        if human_agent:
            self.hint = ttk.Label(
                self, text="Hint: use keyboard arrows to move tiles."
            )
        else:
            self.hint = ttk.Label(
                self, text=""
            )
        self.score = GameScore(self)
        self.hiscore = GameScore(self, label="Highest:")
        self.grid.pack(side=TK.TOP, padx=self._padding, pady=self._padding)
        self.hint.pack(side=TK.TOP)
        self.score.pack(side=TK.LEFT)
        self.hiscore.pack(side=TK.LEFT)
        if human_agent:
            ttk.Button(self, text="Ciao!", command=self.quit_app).pack(side=TK.RIGHT, padx=self._padding,
                                                                       pady=self._padding)
            ttk.Button(self, text="New Game", command=self._new_game_callback).pack(side=TK.RIGHT)
        else:
            ttk.Button(self, text="Ciao!", command=self.quit_app, state=TK.DISABLED).pack(side=TK.RIGHT,
                                                                                          padx=self._padding,
                                                                                          pady=self._padding)
            ttk.Button(self, text="New Game", command=self._new_game_callback, state=TK.DISABLED).pack(side=TK.RIGHT)

    def center_window(self):
        r"""
        tries to center window along screen dims;

        no return value (void);
        """
        # ensure dims are correct
        self.update_idletasks()
        left = (self.winfo_screenwidth() - self.winfo_reqwidth()) // 2
        top = (self.winfo_screenheight() - self.winfo_reqheight()) // 2
        self.geometry("+{x}+{y}".format(x=left, y=top))

    def initialize(self, initial_game_state):
        r"""
        widget's main inits;
        """
        # main window inits

        # set score callback method

        self.grid.set_score_callback(self.update_score)
        self.withdraw()

        self.unbind_all("<Key>")
        self.listen = True

        self.center_window()
        self.deiconify()
        self.game_state = initial_game_state
        self.grid.reset_grid()
        self.grid.set_game_state(self.game_state)
        self.set_score(self.game_state.score)
        self.bind_all("<Key>", self._keyboard_pressed_listener)

    def _keyboard_pressed_listener(self, tk_event=None, *args, **kw):
        for observable in self._keyboard_pressed_observers:
            observable()(tk_event, *args, **kw)

    def subscribe_to_keyboard_pressed(self, observable):
        self._keyboard_pressed_observers.append(weakref.WeakMethod(observable))

    def set_score(self, value):
        self.score.set_score(value)

    def quit_app(self, **kw):
        r"""
        quit app dialog;
        """
        if tkinter.messagebox.askokcancel("Question", "Quit game?", parent=self):
            self._quit_game_callback()
            self.quit()

    def update_state(self, state, action, opponent_action):
        if action == Action.LEFT:
            self.grid.move_tiles_left()
        elif action == Action.RIGHT:
            self.grid.move_tiles_right()
        elif action == Action.UP:
            self.grid.move_tiles_up()
        elif action == Action.DOWN:
            self.grid.move_tiles_down()
        elif action is Action.STOP:
            pass
        else:
            raise Exception("Got unknown action.")
        self.grid.insert_tile(opponent_action.row, opponent_action.column, opponent_action.value)
        self.mainloop_iteration()

    def mainloop_iteration(self):
        self.update_idletasks()
        self.update()

    def update_score(self, value, mode="add"):
        r"""
        updates score along @value and @mode;
        """

        # relative mode?

        if str(mode).lower() in ("add", "inc", "+"):

            # increment score value

            self.score.add_score(value)

        # absolute mode

        else:

            # set new value

            self.score.set_score(value)

        # end if

        # update high score

        self.hiscore.high_score(self.score.get_score())

    # end def

# end class GabrieleCirulli2048
